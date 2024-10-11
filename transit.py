import streamlit as st
from ui import (
    chart_ui,
    data_form,
    data_obj,
    date_adjustment,
    options_ui,
    stats_ui,
)

id1 = "transit"
id2 = "current"
options_ui()

"##### Transit Chart"

name, city1 = data_form(title="Birth Data", id=id1)
st.write("")
_, city2 = data_form(title="Transit Time & Location", id=id2, transit=True)

if name and city1 and city2:
    data1 = data_obj(name, city1, id1)
    data2 = data_obj(id2, city2, id2)
    chart_ui(data1, data2)
    date_adjustment(id2)
    stats_ui(data1, data2)
