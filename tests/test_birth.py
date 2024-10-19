from datetime import datetime
from pytest import fixture
from streamlit.testing.v1 import AppTest
from streamlit.runtime.state.safe_session_state import SafeSessionState


@fixture(scope="package")
def birth():
    return AppTest.from_file("main.py").run()


@fixture(scope="package")
def sess(birth: AppTest):
    return birth.session_state


id = "d1"
name = f"{id}_name"
city = f"{id}_city"
date = f"{id}_date"
hr = f"{id}_hr"
min = f"{id}_min"


def test_default_name(birth: AppTest):
    assert birth.text_input(key=name).value == ""


def test_default_date(birth: AppTest):
    assert birth.date_input(key=date).value == datetime(2000, 1, 1).date()
    assert birth.selectbox(key=hr).value == 13
    assert birth.selectbox(key=min).value == 0


def test_default_city(birth: AppTest):
    assert birth.selectbox(key=city).value == None


def test_sample_data(birth: AppTest, sess: SafeSessionState):
    birth.text_input(key=name).set_value("sample")
    birth.date_input(key=date).set_value(datetime(1976, 4, 20))
    birth.selectbox(key=hr).set_value(18)
    birth.selectbox(key=min).set_value(58)
    birth.selectbox(key=city).set_value("Hong Kong")
    birth.run()
    assert sess[name] == "sample"
    assert sess[city] == "Hong Kong"
    assert sess[date] == datetime(1976, 4, 20).date()


def test_stats_ui(birth: AppTest, sess: SafeSessionState):
    assert sess[name] == "sample"
    assert "Celestial Bodies (sample)" in birth.markdown[2].value


def test_change_options(birth: AppTest, sess: SafeSessionState):
    birth.selectbox(key="hse_sys").select("Whole_Sign")
    birth.run()
    assert "00°♋00" in birth.markdown[2].value
