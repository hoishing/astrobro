import streamlit as st
from datetime import datetime
from natal.config import Display, Orb
from pydantic import BaseModel
from streamlit.runtime.state.safe_session_state import SafeSessionState
from utils import get_dt


class DataArchive(BaseModel):
    """a hashable data archive of the current chart data"""

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


def archive_obj(sess: SafeSessionState = st.session_state) -> DataArchive:
    """Return a DataArchive object of the current chart data."""
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
    )
