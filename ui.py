import streamlit as st
from const import BODIES, CITY_ASCII
from datetime import datetime, timedelta, date as Date
from natal import Chart, Data, HouseSys, Stats
from natal.config import Config, Display, Orb, ThemeType
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
    st.selectbox("House System", HouseSys._member_names_, index=0, key="hse_sys")
    st.selectbox("Chart Theme", ThemeType.__args__, index=1, key="theme")
    st.slider("Chart Size", 400, 1000, 650, 50, key="chart_size")


def orb_opt():
    orb = Orb()
    for aspect in ASPECT_NAMES:
        st.number_input(
            label=aspect,
            min_value=1,
            max_value=10,
            value=orb[aspect],
            key=aspect,
        )


def display_opt(num: int):
    display = Display()
    for body in BODIES:
        st.toggle(body, display[body], key=f"{body}{num}")


def date_adjustment(id: str):
    c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
    unit = c2.selectbox(
        "date adjustment",
        ["year", "month", "week", "day", "hour", "minute"],
        index=3,
        label_visibility="collapsed",
    )
    with c1:
        button(
            "❮", "alt+arrowleft", on_click=adjust_date, args=(id, unit, -1), key="prev"
        )
    with c3:
        button(
            "❯", "alt+arrowright", on_click=adjust_date, args=(id, unit, 1), key="next"
        )


def chart_ui(data1: Data, data2: Data = None):
    chart = Chart(data1=data1, data2=data2, width=sess.chart_size)
    st.write("")
    with st.container(key="chart"):
        st.image(chart.svg, width=sess.chart_size)


def stats_ui(data1: Data, data2: Data = None):
    stats = Stats(data1=data1, data2=data2)
    st.markdown(stats.full_report("html"), unsafe_allow_html=True)
    st.write("")


# utils ======================================================


def adjust_date(id: str, unit: str, shift: Literal[1, -1]):
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
    orb = {aspect: sess[aspect] for aspect in ASPECT_NAMES}
    display1 = {body: sess[f"{body}1"] for body in BODIES}

    data1 = Data(
        name=name1,
        city=city1,
        dt=get_dt(id1),
        house_sys=house_sys,
        config=Config(orb=orb, display=display1),
    )

    if name2 and city2 and id2:
        display2 = {body: sess[f"{body}2"] for body in BODIES}
        data2 = Data(
            name=name2,
            city=city2,
            dt=get_dt(id2),
            house_sys=house_sys,
            config=Config(orb=orb, display=display2),
        )
    else:
        data2 = None

    return data1, data2


def get_dt(id: str, date: Date = None, hr: int = None, minute: int = None) -> datetime:
    date = date or sess.get(f"{id}_date")
    hr = hr or sess.get(f"{id}_hr")
    minute = minute or sess.get(f"{id}_min")
    return datetime(date.year, date.month, date.day, hr, minute)
