import streamlit as st
from const import BODIES, CITY_ASCII
from datetime import datetime, timedelta, date as Date
from natal import Chart, Data, HouseSys, Stats
from natal.config import Config, Display, Orb, ThemeType, Chart as ChartConfig
from natal.const import ASPECT_NAMES
from streamlit_shortcuts import button
from typing import Literal

sess = st.session_state


def data_form(id: str, name: str, default_dt: datetime):
    dt = sess.get(f"{id}_dt", default_dt)

    c1, c2 = st.columns(2)
    chart_name = c1.text_input("Name", name, key=f"{id}_name")
    city = c2.selectbox(
        "City", CITY_ASCII, index=None, key=f"{id}_city", help="type to search"
    )

    c1, c2, c3 = st.columns(3)
    c1.date_input(
        "Date",
        value=dt.date(),
        max_value=datetime(2300, 1, 1),
        min_value=datetime(1800, 1, 1),
        format="YYYY-MM-DD",
        key=f"{id}_date",
        on_change=lambda: setattr(
            sess, f"{id}_dt", get_dt(id, date=sess[f"{id}_date"])
        ),
    )
    c2.selectbox(
        "Hour",
        range(24),
        index=dt.hour,
        key=f"{id}_hr",
        on_change=lambda: setattr(sess, f"{id}_dt", get_dt(id, hr=sess[f"{id}_hr"])),
    )
    c3.selectbox(
        "Minute",
        range(60),
        index=dt.minute,
        key=f"{id}_min",
        help="daylight saving time",
        on_change=lambda: setattr(
            sess, f"{id}_dt", get_dt(id, minute=sess[f"{id}_min"])
        ),
    )

    return chart_name, city


def general_opt():
    st.toggle("Show Statistics", key="show_stats")
    c1, c2 = st.columns(2)
    c1.selectbox("House System", HouseSys._member_names_, index=0, key="hse_sys")
    c2.selectbox("Chart Theme", ThemeType.__args__, index=1, key="theme")
    st.slider("Chart Size", 400, 700, 600, 50, key="chart_size")


def orb_opt():
    orb = sess.get("orb", Orb())
    for aspect in ASPECT_NAMES:
        st.number_input(
            label=aspect,
            min_value=0,
            max_value=10,
            value=orb[aspect],
            on_change=lambda: setattr(sess, "orb", get_orb()),
            key=aspect,
        )
    sess["orb"] = orb

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
    display = sess.get(f"display{num}", Display())

    def toggle(body: str):
        st.toggle(
            body,
            display[body],
            key=f"{body}{num}",
            on_change=lambda: setattr(sess, f"display{num}", get_displays(num)),
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


def stepper(id: str):
    with st.container(key=f"stepper"):
        c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
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
    chart = Chart(data1=data1, data2=data2, width=sess.chart_size)
    html = f"<div class='chart_svg'>{chart.styled_svg}</div>"
    st.write("")
    st.markdown(html, unsafe_allow_html=True)


def stats_ui(data1: Data, data2: Data = None):
    stats = Stats(data1=data1, data2=data2)
    st.markdown(stats.full_report("html"), unsafe_allow_html=True)
    st.write("")


# utils ======================================================


def step(id: str, unit: str, shift: Literal[1, -1]):
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

    sess[f"{id}_dt"] = dt


def data_obj(
    name1: str,
    city1: str,
    id1: str,
    name2: str = None,
    city2: str = None,
    id2: str = None,
):
    house_sys = HouseSys[sess[f"hse_sys"]]
    orb = sess.orb
    # orb = {aspect: sess[aspect] for aspect in ASPECT_NAMES}
    display1 = {body: sess[f"{body}1"] for body in BODIES}
    chart = ChartConfig(font="Noto Sans Symbols, Cardo, Arial Unicode MS, sans-serif")

    data1 = Data(
        name=name1,
        city=city1,
        dt=get_dt(id1),
        house_sys=house_sys,
        config=Config(orb=orb, display=display1, chart=chart),
    )

    if name2 and city2 and id2:
        display2 = {body: sess[f"{body}2"] for body in BODIES}
        data2 = Data(
            name=name2,
            city=city2,
            dt=get_dt(id2),
            house_sys=house_sys,
            config=Config(orb=orb, display=display2, chart=chart),
        )
    else:
        data2 = None

    return data1, data2


def get_dt(id: str, date: Date = None, hr: int = None, minute: int = None) -> datetime:
    date = date or sess.get(f"{id}_date")
    hr = hr or sess.get(f"{id}_hr")
    minute = minute or sess.get(f"{id}_min")
    return datetime(date.year, date.month, date.day, hr, minute)


def get_orb():
    return Orb(**{aspect: sess[aspect] for aspect in ASPECT_NAMES})


def set_orbs(vals: list[int]):
    for aspect, val in zip(ASPECT_NAMES, vals):
        sess.orb[aspect] = val


def get_displays(num: int):
    return Display(**{body: sess[f"{body}{num}"] for body in BODIES})


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
