import streamlit as st
from ui import chart_ui, data_form, data_obj, date_adjustment, options_ui, stats_ui

id1 = "s1"
id2 = "s2"
options_ui()

"##### Transit Chart"

name1, city1 = data_form(title="Your Birth Data", id=id1)
st.write("")
name2, city2 = data_form(title="Partner's Birth Data", id=id2)

if name1 and city1 and name2 and city2:
    data1 = data_obj(name1, city1, id1)
    data2 = data_obj(name2, city2, id2)
    chart_ui(data1, data2)
    date_adjustment(id2)
    stats_ui(data1, data2)
