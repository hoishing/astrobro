from datetime import date, datetime
from pytest import fixture
from streamlit.testing.v1 import AppTest
from streamlit.runtime.state.safe_session_state import SafeSessionState


@fixture(scope="package")
def transit():
    return AppTest.from_file("transit.py", default_timeout=10000).run()


@fixture(scope="package")
def sess(transit: AppTest):
    return transit.session_state


id1 = "transit"
name1 = f"{id1}_name"
city1 = f"{id1}_city"
dt1 = f"{id1}_dt"
name_box1 = f"{id1}_name_box"
date_box1 = f"{id1}_date_box"
hr_box1 = f"{id1}_hr_box"
min_box1 = f"{id1}_min_box"
city_box1 = f"{id1}_city_box"

id2 = "current"
city2 = f"{id2}_city"
dt2 = f"{id2}_dt"
date_box2 = f"{id2}_date_box"
hr_box2 = f"{id2}_hr_box"
min_box2 = f"{id2}_min_box"
city_box2 = f"{id2}_city_box"


def test_page_title(transit: AppTest):
    assert transit.markdown[0].value == "##### Transit Chart"


def test_default_date(transit: AppTest):
    assert transit.date_input(key=date_box2).value == date.today()


def test_sample_data(transit: AppTest, sess: SafeSessionState):
    transit.text_input(key=name_box1).set_value("sample")
    transit.date_input(key=date_box1).set_value(date(1976, 4, 20))
    transit.selectbox(key=hr_box1).set_value(18)
    transit.selectbox(key=min_box1).set_value(58)
    transit.selectbox(key=city_box1).set_value("Hong Kong")

    transit.date_input(key=date_box2).set_value(date(2024, 4, 20))
    transit.selectbox(key=hr_box2).set_value(18)
    transit.selectbox(key=min_box2).set_value(58)
    transit.selectbox(key=city_box2).set_value("Hong Kong")

    transit.run()
    assert sess[name1] == "sample"
    assert sess[city1] == "Hong Kong"
    assert sess[dt1] == datetime(1976, 4, 20, 18, 58)
    assert sess[city2] == "Hong Kong"
    assert sess[dt2] == datetime(2024, 4, 20, 18, 58)


def test_adjust_date(transit: AppTest, sess: SafeSessionState):
    transit.button(key=f"next").click().run()
    assert sess[dt2] == datetime(2024, 4, 21, 18, 58)
