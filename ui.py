import sass
import streamlit as st
from datetime import datetime, timedelta
from natal import Chart, Config, Data, HouseSys, Stats, ThemeType
from typing import Literal
from streamlit_shortcuts import button
from natal import Chart, Data, Stats

sess = st.session_state

SOURCE_CODE = """\
![github](https://api.iconify.design/bi/github.svg?color=%236FD886&width=20) &nbsp;
[source code](https://github.com/hoishing/astrobro)
"""

ABOUT = f"💫 &nbsp;AstroBro :&nbsp; your pocket astrologer\n\n{SOURCE_CODE}"

CHART_WIDTH = 680
page_config = dict(
    page_title="AstroBro",
    page_icon="💫",
    menu_items={
        "About": ABOUT,
        "Get help": "https://github.com/hoishing/astrobro/issues",
    },
)

CITY_ASCII = Data.cities.iloc[:, 1]

AdjUnit = Literal["year", "month", "week", "day", "hour", "minute"]


# def city_info(city: str):
#     return Data.cities[Data.cities["ascii_name"] == city].iloc[0]


def data_form(
    title: str,
    id: str,
    transit: bool = False,
):
    with st.expander(title, expanded=True):
        dt_key = f"{id}_dt"
        name_key = f"{id}_name"
        city_key = f"{id}_city"
        city = sess.get(city_key, None)
        city_idx = CITY_ASCII.eq(city).idxmax() if city else None
        dt = sess.get(dt_key, datetime(2000, 1, 1, 12, 0))
        if transit:
            sess[name_key] = None
        else:
            sess[name_key] = st.text_input(
                "Name", sess.get(name_key, None), key=f"{id}_name_box"
            )

        c1, c2, c3 = st.columns(3)
        date = c1.date_input(
            "Date",
            value="today" if transit else dt,
            max_value=datetime(2300, 1, 1),
            min_value=datetime(1800, 1, 1),
            format="YYYY-MM-DD",
            key=f"{id}_date_box",
        )
        hr = c2.selectbox("Hour (24)", range(24), index=dt.hour, key=f"{id}_hr_box")
        min = c3.selectbox("Minute", range(60), index=dt.minute, key=f"{id}_min_box")

        sess[dt_key] = datetime(date.year, date.month, date.day, hr, min)
        sess[city_key] = st.selectbox(
            "City",
            CITY_ASCII,
            index=city_idx,
            key=f"{id}_city_box",
            help="type to search",
        )
        
        return sess[name_key], sess[city_key]


def options_ui():
    with st.sidebar:
        with st.expander("Settings"):
            sys_name = st.selectbox(
                "House System",
                HouseSys._member_names_,
                index=sess.get("hse_sys_idx", 0),
                key="house_sys",
            )
            theme = st.selectbox(
                "Theme",
                ThemeType.__args__,
                index=sess.get("theme_idx", 0),
                key="theme",
            )
        st.markdown(SOURCE_CODE)

    sess["theme_idx"] = ThemeType.__args__.index(theme)
    sess["hse_sys_idx"] = HouseSys._member_names_.index(sys_name)
    sess["config"] = Config(theme_type=theme)
    sess["hse_sys"] = HouseSys[sys_name]


def date_adjustment(id: str):
    c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
    unit = c2.selectbox(
        "date adjustment",
        AdjUnit.__args__,
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


def chart_ui(chart: Chart):
    st.write("")
    st.image(chart.svg)


def stats_ui(stats: Stats):
    # TODO: compile to css and save to static folder
    css = sass.compile(filename="style.scss")
    style = f"<style>{css}</style>"
    st.markdown(style, unsafe_allow_html=True)
    st.html(stats.full_report("html"))
    st.write("")


# utils ======================================================


def adjust_date(id: str, unit: AdjUnit, shift: Literal[1, -1]):
    dt = sess[f"{id}_dt"]

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


def chart_obj(data1: Data, data2: Data = None):
    return Chart(data1=data1, data2=data2, width=CHART_WIDTH, config=sess.config)


def data_obj(name: str, city: str, id: str):
    return Data(name=name, city=city, dt=sess[f"{id}_dt"], house_sys=sess.hse_sys)
