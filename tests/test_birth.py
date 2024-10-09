from datetime import date, datetime
from pytest import fixture
from streamlit.testing.v1 import AppTest
from streamlit.runtime.state.safe_session_state import SafeSessionState


@fixture(scope="package")
def birth_page():
    return AppTest.from_file("birth.py").run()

@fixture(scope="package")
def sess(birth_page: AppTest):
    return birth_page.session_state


id = "birth"
name = f"{id}_name"
city = f"{id}_city"
dt = f"{id}_dt"
name_box = f"{id}_name_box"
date_box = f"{id}_date_box"
hr_box = f"{id}_hr_box"
min_box = f"{id}_min_box"
city_box = f"{id}_city_box"

def test_page_title(birth_page: AppTest):
    assert birth_page.markdown[0].value == "##### Birth Chart"


def test_default_name(birth_page: AppTest):
    assert birth_page.text_input(key=name_box).value == None


def test_default_date(birth_page: AppTest):
    assert birth_page.date_input(key=date_box).value == date(2000, 1, 1)
    assert birth_page.selectbox(key=hr_box).value == 12
    assert birth_page.selectbox(key=min_box).value == 0


def test_default_city(birth_page: AppTest):
    assert birth_page.selectbox(key=city_box).value == None


def test_shing_data(birth_page: AppTest, sess: SafeSessionState):
    birth_page.text_input(key=name_box).set_value("shing")
    birth_page.date_input(key=date_box).set_value(date(1976, 4, 20))
    birth_page.selectbox(key=hr_box).set_value(18)
    birth_page.selectbox(key=min_box).set_value(58)
    birth_page.selectbox(key=city_box).set_value("Hong Kong")
    birth_page.run()
    assert sess[name] == "shing"
    assert sess[city] == "Hong Kong"
    assert sess[dt] == datetime(1976, 4, 20, 18, 58)


def test_stats_ui(birth_page: AppTest, sess: SafeSessionState):
    assert sess[name] == "shing"
    assert 'Celestial Bodies (shing)' in birth_page.markdown[3].value