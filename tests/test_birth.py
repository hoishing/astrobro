from datetime import date, datetime
from pytest import fixture
from streamlit.testing.v1 import AppTest
from streamlit.runtime.state.safe_session_state import SafeSessionState


@fixture(scope="package")
def birth():
    return AppTest.from_file("birth.py").run()

@fixture(scope="package")
def sess(birth: AppTest):
    return birth.session_state


id = "birth"
name = f"{id}_name"
city = f"{id}_city"
dt = f"{id}_dt"
name_box = f"{id}_name_box"
date_box = f"{id}_date_box"
hr_box = f"{id}_hr_box"
min_box = f"{id}_min_box"
city_box = f"{id}_city_box"

def test_page_title(birth: AppTest):
    assert birth.markdown[0].value == "##### Birth Chart"


def test_default_name(birth: AppTest):
    assert birth.text_input(key=name_box).value == None


def test_default_date(birth: AppTest):
    assert birth.date_input(key=date_box).value == date(2000, 1, 1)
    assert birth.selectbox(key=hr_box).value == 12
    assert birth.selectbox(key=min_box).value == 0


def test_default_city(birth: AppTest):
    assert birth.selectbox(key=city_box).value == None


def test_sample_data(birth: AppTest, sess: SafeSessionState):
    birth.text_input(key=name_box).set_value("sample")
    birth.date_input(key=date_box).set_value(date(1976, 4, 20))
    birth.selectbox(key=hr_box).set_value(18)
    birth.selectbox(key=min_box).set_value(58)
    birth.selectbox(key=city_box).set_value("Hong Kong")
    birth.run()
    assert sess[name] == "sample"
    assert sess[city] == "Hong Kong"
    assert sess[dt] == datetime(1976, 4, 20, 18, 58)


def test_stats_ui(birth: AppTest, sess: SafeSessionState):
    assert sess[name] == "sample"
    assert 'Celestial Bodies (sample)' in birth.markdown[3].value

def test_change_options(birth: AppTest, sess: SafeSessionState):
    birth.selectbox(key="hse_sys").select("Whole_Sign")
    birth.run()
    assert '00°♋00' in birth.markdown[3].value
