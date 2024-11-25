import streamlit as st
from archive import archive_str, get_dt, import_data
from const import BODIES, CITY_ASCII
from datetime import date as Date
from datetime import datetime, timedelta
from io import BytesIO
from natal import Chart, Data, HouseSys, Stats
from natal.config import Config, Display, Orb, ThemeType
from natal.const import ASPECT_NAMES
from natal.report import Report
from streamlit_shortcuts import button
from typing import Literal

sess = st.session_state


def data_form(id: int):
    sess[f"name{id}"] = sess.get(f"name{id}", "" if id == 1 else "transit")
    sess[f"city{id}"] = sess.get(f"city{id}", None)
    c1, c2 = st.columns(2)
    name = c1.text_input("Name", key=f"name{id}")
    city = c2.selectbox("City", CITY_ASCII, key=f"city{id}", help="type to sarch")
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
    with c2:
        filename, name1, city1, *_ = input_status()
        ready = name1 and city1
        with st.empty():
            if st.button("Generate PDF", use_container_width=True, disabled=not ready):
                with st.spinner("generating..."):
                    pdf = pdf_report()
                st.download_button(
                    ":material/download: Download",
                    pdf,
                    file_name=f"{filename}_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
    sess["house_sys"] = sess.get("house_sys", "Placidus")
    sess["theme_type"] = sess.get("theme_type", "dark")
    c1, c2 = st.columns(2)
    c1.selectbox("House System", HouseSys._member_names_, key="house_sys")
    c2.selectbox("Chart Theme", ThemeType.__args__, key="theme_type")
    st.slider("Chart Size", 300, 1200, 600, 50, key="chart_size")


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


def save_load_ui():
    filename, name1, city1, *_ = input_status()
    data1_ready = name1 and city1

    with st.expander("save / load data", expanded=True):
        st.download_button(
            "save chart data",
            archive_str() if data1_ready else "",
            file_name=f"{filename}.json",
            use_container_width=True,
            key="save_button",
            disabled=not data1_ready,
        )
        st.file_uploader(
            "load chart data",
            key="load_file",
            on_change=lambda: import_data(sess.load_file),
        )


def stepper(id: int):
    with st.container(key="stepper"):
        c1, c2, c3 = st.columns([3, 4, 3], vertical_alignment="bottom")
        with c2:
            unit = st.selectbox(
                "date adjustment",
                ["year", "month", "week", "day", "hour", "minute"],
                index=3,
                label_visibility="collapsed",
            )
        with c1:
            button("❮", "alt+arrowleft", on_click=step, args=(id, unit, -1), key="prev")
        with c3:
            button("❯", "alt+arrowright", on_click=step, args=(id, unit, 1), key="next")


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
    house_sys = HouseSys[sess["house_sys"]]
    orb = sess.orb
    display1 = {body: sess[f"{body}1"] for body in BODIES}

    data1 = Data(
        name=name1,
        city=city1,
        dt=get_dt(1),
        config=Config(
            house_sys=house_sys, theme_type=sess.theme_type, orb=orb, display=display1
        ),
    )

    if name2 and city2:
        display2 = {body: sess[f"{body}2"] for body in BODIES}
        orb2 = Orb(**{aspect: 0 for aspect in ASPECT_NAMES})
        data2 = Data(
            name=name2,
            city=city2,
            dt=get_dt(2),
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


def pdf_report() -> BytesIO | str:
    _, name1, city1, name2, city2 = input_status()
    if name1 and city1:
        data1, data2 = data_obj(name1, city1, name2, city2)
        report = Report(data1, data2)
        return report.create_pdf(report.full_report)
    else:
        return ""


def input_status() -> tuple[str, bool, bool, str, str, str, str]:
    name1 = sess.get("name1")
    city1 = sess.get("city1")
    name2 = sess.get("name2")
    city2 = sess.get("city2")
    filename = f"{name1}_{name2}" if (name2 and city2) else name1
    return filename, name1, city1, name2, city2
