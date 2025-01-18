import streamlit as st
from datetime import datetime
from io import BytesIO
from natal.config import Display, Orb
from pydantic import BaseModel
from streamlit.runtime.state.safe_session_state import SafeSessionState
from utils import get_dt


class DataArchive(BaseModel):
    name1: str
    city1: str | None = None
    dt1: datetime
    name2: str
    city2: str | None = None
    dt2: datetime | None = None
    house_sys: str
    theme_type: str
    orb: Orb
    display1: Display
    display2: Display


def archive_str(sess: SafeSessionState = st.session_state) -> str:
    """Return a JSON string of the current chart data."""
    return DataArchive(
        name1=sess.name1,
        city1=sess.city1,
        dt1=get_dt(1, sess),
        name2=sess.name2,
        city2=sess.city2,
        dt2=get_dt(2, sess) if (sess.name2 and sess.city2) else None,
        house_sys=sess.house_sys,
        theme_type=sess.theme_type,
        orb=sess.orb,
        display1=sess.display1,
        display2=sess.display2,
    ).model_dump_json()


def import_data(fp: BytesIO | None, sess: SafeSessionState = st.session_state):
    """Import chart data from a JSON file."""
    if not fp:
        return
    data = DataArchive.model_validate_json(fp.read())
    sess.name1 = data.name1
    sess.city1 = data.city1
    sess.date1 = data.dt1.date()
    sess.hr1 = data.dt1.hour
    sess.min1 = data.dt1.minute
    sess.name2 = data.name2
    sess.city2 = data.city2
    sess.date2 = data.dt2.date() if data.dt2 else None
    sess.hr2 = data.dt2.hour if data.dt2 else 0
    sess.min2 = data.dt2.minute if data.dt2 else 0
    sess.house_sys = data.house_sys
    sess.theme_type = data.theme_type
    sess.display1 = data.display1
    sess.display2 = data.display2
    sess.orb = data.orb
