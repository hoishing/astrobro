import streamlit as st
from natal import Data, Chart, HouseSys
from datetime import date, datetime, time
from utils import page_config, header

st.set_page_config(**page_config)

header("Natal Chart")


data1_name = st.text_input("Name")
c1, c2, c3 = st.columns(3)
data1_date = c1.date_input("Date", value=date(2000, 1, 1))
data1_hr = c2.selectbox("Hour", range(24), index=12)
data1_min = c3.selectbox("Minute", range(60), index=0)
data1_city = st.selectbox("City of Birth", Data.cities, index=None)
chart1_house_system = st.selectbox("House System", HouseSys._member_names_)

if st.button("Generate Chart"):
    city1 = Data.cities[Data.cities["name"] == data1_city].iloc[0]
    data1 = Data(
        name=data1_name,
        dt=datetime.combine(data1_date, time(hour=data1_hr, minute=data1_min)),
        city=city1.ascii_name,
        house_sys=HouseSys[chart1_house_system],
    )
    st.write(data1)
