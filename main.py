import streamlit as st
from datetime import datetime
from const import PAGE_CONFIG, STYLE, LOGO
from ui import (
    chart_ui,
    data_form,
    data_obj,
    date_adjustment,
    display_ui,
    options_ui,
    orb_ui,
    stats_ui,
)

st.set_page_config(**PAGE_CONFIG)
st.logo(LOGO)
st.markdown(STYLE, unsafe_allow_html=True)

id1 = "d1"
id2 = "d2"

with st.sidebar:
    options_ui()
    with st.expander("Orbs"):
        orb_ui()
    with st.expander("Birth Data Entities"):
        display_ui(1)
    with st.expander("Transit / Synastry Entities"):
        display_ui(2)


with st.expander("Birth Data", expanded=True):
    name1, city1 = data_form(id1, "", datetime(2000, 1, 1, 13, 0))

with st.expander("Transit / Synastry"):
    name2, city2 = data_form(id2, "Current", datetime.now())

if name1 and city1:
    data1, data2 = data_obj(name1, city1, id1, name2, city2, id2)
    chart_ui(data1, data2)
    date_adjustment(id2 if data2 else id1)
    stats_ui(data1, data2)
