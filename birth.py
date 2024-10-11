from ui import (
    chart_ui,
    data_form,
    data_obj,
    date_adjustment,
    options_ui,
    stats_ui,
)

# data_from id
id = "birth"
options_ui()

"##### Birth Chart"

name, city = data_form(title="Birth Data", id=id)

if name and city:
    data = data_obj(name, city, id)
    chart_ui(data)
    date_adjustment(id)
    stats_ui(data)
