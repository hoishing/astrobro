import pandas as pd
import streamlit as st
from archive import archive_obj
from const import BODIES
from datetime import date as Date
from datetime import datetime, timedelta
from natal import Chart, Data, HouseSys, Stats
from natal.config import Config, Display, Orb, ThemeType
from natal.const import ASPECT_NAMES
from streamlit_local_storage import LocalStorage
from streamlit_shortcuts import shortcut_button
from typing import Literal
from utils import charts_data, get_cities, get_dt, utc_of

# constants ===============================================
sess = st.session_state
local_storage = LocalStorage()
sess.setdefault("all_charts", local_storage.getItem("all_charts") or [])

# ui ======================================================


def data_form(id: int):
    sess[f"name{id}"] = sess.get(f"name{id}", "" if id == 1 else "transit")
    sess[f"city{id}"] = sess.get(f"city{id}", None)
    c1, c2 = st.columns(2)
    name = c1.text_input("Name", key=f"name{id}")
    city = c2.selectbox(
        "City", get_cities().index, key=f"city{id}", help="type to search"
    )
    now = datetime.now()
    sess[f"date{id}"] = sess.get(f"date{id}") or (
        Date(2000, 1, 1) if id == 1 else now.date()
    )
    sess[f"hr{id}"] = sess.get(f"hr{id}", 13 if id == 1 else now.hour)
    sess[f"min{id}"] = sess.get(f"min{id}", 0 if id == 1 else now.minute)
    c1, c2, c3 = st.columns(3)
    c1.date_input(
        "Date",
        max_value=Date(2300, 1, 1),
        min_value=Date(1800, 1, 1),
        format="YYYY-MM-DD",
        key=f"date{id}",
    )
    c2.selectbox(
        "Hour",
        range(24),
        key=f"hr{id}",
    )
    c3.selectbox(
        "Minute",
        range(60),
        key=f"min{id}",
        help="daylight saving time",
    )

    return name, city


def general_opt():
    c1, c2 = st.columns(2)
    c1.toggle("Show Statistics", key="show_stats")
    # with c2:
    #     filename, name1, city1, *_ = input_status()
    #     ready = name1 and city1
    #     with st.empty():
    #         if st.button("Generate PDF", use_container_width=True, disabled=not ready):
    #             with st.spinner("generating..."):
    #                 pdf = pdf_report()
    #             st.download_button(
    #                 ":material/download: Download",
    #                 pdf,
    #                 file_name=f"{filename}_report.pdf",
    #                 mime="application/pdf",
    #                 use_container_width=True,
    #             )
    sess["house_sys"] = sess.get("house_sys", "Placidus")
    sess["theme_type"] = sess.get("theme_type", "dark")
    c1, c2 = st.columns(2)
    c1.selectbox("House System", HouseSys._member_names_, key="house_sys")
    c2.selectbox("Chart Theme", ThemeType.__args__, key="theme_type")
    # st.slider("Chart Size", 300, 1200, 600, 50, key="chart_size")


def orb_opt():
    sess.orb = sess.get("orb", Orb())
    for aspect in ASPECT_NAMES:
        st.number_input(
            label=aspect,
            value=sess.orb[aspect],
            min_value=0,
            max_value=10,
            # actualize at change time, loop causes `aspect` stick to last value
            on_change=lambda asp: sess.orb.update({asp: sess[asp]}),
            args=(aspect,),  # actualize at create time
            key=aspect,
        )

    c1, c2, c3 = st.columns(3)
    c1.button(
        "disable",
        key="disable_orbs",
        use_container_width=True,
        on_click=lambda: set_orbs([0, 0, 0, 0, 0]),
    )
    c2.button(
        "transit",
        key="transit_orbs",
        use_container_width=True,
        on_click=lambda: set_orbs([2, 2, 2, 2, 1]),
    )
    c3.button(
        "default",
        key="default_orbs",
        use_container_width=True,
        on_click=lambda: set_orbs(Orb().model_dump().values()),
    )


def display_opt(num: int):
    display_n = f"display{num}"
    sess[display_n] = sess.get(display_n, Display())

    def toggle(body: str):
        body_n = f"{body}{num}"
        sess[body_n] = sess[display_n][body]
        st.toggle(
            body,
            key=body_n,
            # actualize at change time, won't stick to loop last value because its scoped by the enclosing function
            on_change=lambda: sess[display_n].update({body: sess[body_n]}),
        )

    c1, c2 = st.columns(2)
    with c1:
        for body in BODIES[:10]:
            toggle(body)
    with c2:
        for body in BODIES[10:]:
            toggle(body)

    c1, c2 = st.columns(2)
    c1.button(
        "inner planets",
        key=f"inner_display{num}",
        use_container_width=True,
        on_click=lambda: set_displays(num, "inner"),
    )
    c2.button(
        "default",
        key=f"default_display{num}",
        use_container_width=True,
        on_click=lambda: set_displays(num, "default"),
    )


def saved_charts_ui():
    """Display saved charts from localStorage with `st.data_editor`."""
    st.subheader("Saved Charts")

    # Check if localStorage is available
    if not sess.all_charts:
        st.info("localStorage not available. Save a chart first to initialize.")
        return

    df = pd.DataFrame(charts_data(sess.all_charts))
    display_names = ["Name 1", "City 1", "Date 1", "Name 2", "City 2", "Date 2"]
    df.columns = display_names + list(df.columns[len(display_names) :])

    # Display the dataframe with the requested columns
    st.data_editor(df, use_container_width=True, hide_index=True, num_rows="dynamic")


def save_load_ui():
    name1, city1, *_ = input_states()
    data1_ready = name1 and city1
    if "all_charts" not in sess:
        sess["all_charts"] = local_storage.getItem("all_charts") or dict()

    with st.expander("saved charts", expanded=True):
        # Save to localStorage button
        if st.button(
            "save chart data",
            use_container_width=True,
            key="save_button",
            disabled=not data1_ready,
        ):
            archive = archive_obj()
            json_str = archive.model_dump_json()
            sess.all_charts[hash(json_str)] = json_str
            local_storage.setItem("all_charts", sess.all_charts)
            st.success("Chart saved!")

        # Display saved charts
        saved_charts_ui()


def stepper(id: int):
    with st.container(key="stepper"):
        st.write("")
        c1, c2, c3 = st.columns([3, 4, 3])
        with c2:
            unit = st.selectbox(
                "date adjustment",
                ["year", "month", "week", "day", "hour", "minute"],
                index=3,
                label_visibility="collapsed",
            )
        with c1:
            shortcut_button(
                "❮",
                "alt+arrowleft",
                hint=False,
                on_click=step,
                args=(id, unit, -1),
                key="prev",
            )
        with c3:
            shortcut_button(
                "❯",
                "alt+arrowright",
                hint=False,
                on_click=step,
                args=(id, unit, 1),
                key="next",
            )


def chart_ui(data1: Data, data2: Data = None):
    st.write("")
    chart = Chart(data1=data1, data2=data2, width=sess.chart_size)
    with st.container(key="chart_svg"):
        st.markdown(chart.svg, unsafe_allow_html=True)


def stats_ui(data1: Data, data2: Data = None):
    stats = Stats(data1=data1, data2=data2)
    st.markdown(stats.full_report("html"), unsafe_allow_html=True)
    st.write("")


# utils ======================================================


def step(id: int, unit: str, shift: Literal[1, -1]):
    dt = get_dt(id)

    match unit:
        case "week":
            delta = timedelta(weeks=shift)
        case "day":
            delta = timedelta(days=shift)
        case "hour":
            delta = timedelta(hours=shift)
        case "minute":
            delta = timedelta(minutes=shift)
        case "month":
            new_month = dt.month + shift
            new_year = dt.year + (new_month - 1) // 12
            new_month = ((new_month - 1) % 12) + 1
            dt = dt.replace(year=new_year, month=new_month)
        case "year":
            dt = dt.replace(year=dt.year + shift)

    if unit not in ["month", "year"]:
        dt += delta

    sess[f"date{id}"] = dt.date()
    sess[f"hr{id}"] = dt.hour
    sess[f"min{id}"] = dt.minute


def data_obj(
    name1: str,
    city1: str,
    name2: str = None,
    city2: str = None,
):
    def get_params(id: int, city: str) -> dict:
        city_info = get_cities().loc[city]
        lat_lon = city_info[["lat", "lon"]].to_dict()
        lat_lon["utc_dt"] = utc_of(get_dt(id), city_info["timezone"])
        return lat_lon

    house_sys = HouseSys[sess["house_sys"]]
    orb = sess.orb
    display1 = {body: sess[f"{body}1"] for body in BODIES}

    data1 = Data(
        name=name1,
        **get_params(1, city1),
        config=Config(
            house_sys=house_sys, theme_type=sess.theme_type, orb=orb, display=display1
        ),
    )

    if name2 and city2:
        display2 = {body: sess[f"{body}2"] for body in BODIES}
        orb2 = Orb(**{aspect: 0 for aspect in ASPECT_NAMES})
        data2 = Data(
            name=name2,
            **get_params(2, city2),
            config=Config(house_sys=house_sys, orb=orb2, display=display2),
        )
    else:
        data2 = None

    return data1, data2


def set_orbs(vals: list[int]):
    for aspect, val in zip(ASPECT_NAMES, vals):
        sess.orb[aspect] = val


def set_displays(num: int, opt: Literal["inner", "planets", "default"]):
    display = dict.fromkeys(BODIES, False)
    inner = ["asc", "sun", "moon", "mercury", "venus", "mars"]
    match opt:
        case "inner":
            display.update(dict.fromkeys(inner, True))
        case "planets":
            planets = inner + ["jupiter", "saturn", "uranus", "neptune", "pluto"]
            display.update(dict.fromkeys(planets, True))
        case "default":
            display = Display()

    sess[f"display{num}"] = Display(**display)


# def pdf_report() -> BytesIO | str:
#     name1, city1, name2, city2 = input_states()
#     if name1 and city1:
#         data1, data2 = data_obj(name1, city1, name2, city2)
#         # report = Report(data1, data2)
#         # return report.create_pdf(report.full_report)
#         return ""
#     else:
#         return ""


def input_states() -> tuple[str, str, str, str]:
    name1 = sess.get("name1")
    city1 = sess.get("city1")
    name2 = sess.get("name2")
    city2 = sess.get("city2")
    return name1, city1, name2, city2


def load_chart_from_json_data(json_str: str):
    """Load chart data from JSON string into session state."""
    try:
        from archive import DataArchive

        data = DataArchive.model_validate_json(json_str)

        sess.name1 = data.name1
        sess.city1 = data.city1
        sess.date1 = data.dt1.date()
        sess.hr1 = data.dt1.hour
        sess.min1 = data.dt1.minute
        sess.name2 = data.name2
        sess.city2 = data.city2
        sess.date2 = data.dt2.date() if data.dt2 else None
        sess.hr2 = data.dt2.hour if data.dt2 else 0
        sess.min2 = data.dt2.minute if data.dt2 else 0
        sess.house_sys = data.house_sys
        sess.theme_type = data.theme_type
        sess.display1 = data.display1
        sess.display2 = data.display2
        sess.orb = data.orb

        st.success("Chart loaded successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to load chart: {e}")


def delete_saved_chart_simple(chart_key: str):
    """Delete chart from localStorage using simple approach."""
    try:
        if sess.get("localStorage"):
            # For streamlit-local-storage, we need to check what delete method is available
            # Let's try to set the item to None/empty to "delete" it
            sess.localStorage.setItem(chart_key, "")

            # Remove from tracked keys
            if "saved_chart_keys" in sess:
                sess.saved_chart_keys.discard(chart_key)

            chart_display_name = chart_key.replace("astrobro_", "")
            st.success(f"Chart '{chart_display_name}' deleted!")
            st.rerun()
        else:
            st.error("localStorage not available")
    except Exception as e:
        st.error(f"Failed to delete chart: {e}")
