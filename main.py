import streamlit as st
from const import LOGO, PAGE_CONFIG, STYLE
from ui import (
    chart_ui,
    data_form,
    data_obj,
    display_opt,
    general_opt,
    orb_opt,
    save_load_ui,
    stats_ui,
    stepper,
)

st.set_page_config(**PAGE_CONFIG)
st.logo(LOGO)
st.markdown(STYLE, unsafe_allow_html=True)

with st.sidebar:
    general_opt()
    with st.expander("Options"):
        t1, t2, t3 = st.tabs(["Orbs", "Birth", "Transit/Synastry"])
        with t1:
            orb_opt()
        with t2:
            display_opt(1)
        with t3:
            display_opt(2)
    save_load_ui()

with st.expander("Birth Data", expanded=True):
    name1, city1 = data_form(1)

with st.expander("Transit / Synastry"):
    name2, city2 = data_form(2)

if name1 and city1:
    data1, data2 = data_obj(name1, city1, name2, city2)
    chart_ui(data1, data2)
    stepper(2 if data2 else 1)
    if st.session_state.show_stats:
        stats_ui(data1, data2)
