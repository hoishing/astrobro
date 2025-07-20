import json
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit.runtime.state.safe_session_state import SafeSessionState
from zoneinfo import ZoneInfo


@st.cache_resource
def get_cities() -> pd.DataFrame:
    """cached cities df, index: location, columns: lat, lon, timezone"""
    df = pd.read_csv("cities.csv.gz")
    location = df["name"] + " - " + df["country"]
    return df[["lat", "lon", "timezone"]].set_index(location)


def utc_of(dt: datetime, timezone: str) -> datetime:
    """convert local datetime to utc datetime

    args:
        dt: local datetime
        timezone: timezone string
    returns:
        utc datetime
    """
    local_tz = ZoneInfo(timezone)
    local_dt = dt.replace(tzinfo=local_tz)
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
    return utc_dt


def get_dt(id: int, sess: SafeSessionState = st.session_state) -> datetime:
    """get datetime from session state

    args:
        id: 1 or 2, for 1st or 2nd person
        sess: current session state
    returns:
        datetime
    """
    date = sess[f"date{id}"]
    hr = sess[f"hr{id}"]
    minute = sess[f"min{id}"]
    return datetime(date.year, date.month, date.day, hr, minute)


@st.cache_data(show_spinner=False)
def charts_data(charts: dict) -> list[dict]:
    data = [json.loads(chart) for chart in charts.values()]
    display_names = ["Name 1", "City 1", "Date 1", "Name 2", "City 2", "Date 2"]
    df = pd.DataFrame(data)
    df.columns = display_names + list(df.columns[len(display_names) :])
    df.index = charts.keys()
    df["Date 1"] = pd.to_datetime(df["Date 1"])
    df["Date 2"] = pd.to_datetime(df["Date 2"])
    return df
