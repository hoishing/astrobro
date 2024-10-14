import streamlit as st
from ui import page_config


birth = st.Page("birth.py", title="Birth Chart", icon=":material/person:")
transit = st.Page("transit.py", title="Transit", icon=":material/arrow_range:")
synastry = st.Page("synastry.py", title="Synastry", icon=":material/group:")

pg = st.navigation([birth, transit, synastry])
st.set_page_config(**page_config)
st.logo(image="static/astrobro-logo.png")
pg.run()
