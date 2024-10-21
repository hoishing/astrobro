from datetime import datetime, date
from pytest import fixture
from streamlit.testing.v1 import AppTest
from streamlit.runtime.state.safe_session_state import SafeSessionState


@fixture(scope="package")
def transit():
    return AppTest.from_file("main.py", default_timeout=10000).run()


@fixture(scope="package")
def sess(transit: AppTest):
    return transit.session_state


id1 = "d1"
name1 = f"{id1}_name"
city1 = f"{id1}_city"
date1 = f"{id1}_date"
hr1 = f"{id1}_hr"
min1 = f"{id1}_min"

id2 = "d2"
name2 = f"{id2}_name"
city2 = f"{id2}_city"
date2 = f"{id2}_date"
hr2 = f"{id2}_hr"
min2 = f"{id2}_min"


def test_default_date(transit: AppTest):
    assert transit.date_input(key=date2).value == date.today()


def test_sample_data(transit: AppTest, sess: SafeSessionState):

    transit.text_input(key=name1).set_value("sample")
    transit.date_input(key=date1).set_value(datetime(1976, 4, 20))
    transit.selectbox(key=hr1).set_value(18)
    transit.selectbox(key=min1).set_value(58)
    transit.selectbox(key=city1).set_value("Hong Kong")

    transit.date_input(key=date2).set_value(datetime(2014, 4, 20))
    transit.selectbox(key=hr2).set_value(18)
    transit.selectbox(key=min2).set_value(48)
    transit.selectbox(key=city2).set_value("Taipei")

    transit.run()

    assert sess[name1] == "sample"
    assert sess[city1] == "Hong Kong"
    assert sess[date1] == date(1976, 4, 20)
    assert sess[hr1] == 18
    assert sess[min1] == 58
    assert sess[city2] == "Taipei"
    assert sess[date2] == date(2014, 4, 20)
    assert sess[hr2] == 18
    assert sess[min2] == 48


def test_next_button(transit: AppTest, sess: SafeSessionState):
    # press next button
    transit.button(key="next").click().run()
    assert transit.date_input(key=date2).value == date(2014, 4, 21)
