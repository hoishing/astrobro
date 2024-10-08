import streamlit as st
from natal import Stats
from ui import (
    chart_obj,
    chart_ui,
    data_form,
    data_obj,
    date_adjustment,
    options_ui,
    sess,
    stats_ui,
)

id = "birth"
options_ui()

"##### Birth Chart"

name, city = data_form(title="Birth Data", id=id)

if name and city:
    data = data_obj(name, city, id)
    chart = chart_obj(data)
    stats = Stats(data)
    chart_ui(chart)
    date_adjustment(id)
    stats_ui(stats)
