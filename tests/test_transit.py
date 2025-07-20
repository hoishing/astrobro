from . import transit_sample
from datetime import date
from pytest import fixture
from streamlit.runtime.state.safe_session_state import SafeSessionState
from streamlit.testing.v1 import AppTest


@fixture(scope="package")
def transit():
    return AppTest.from_file("main.py", default_timeout=10000).run()


@fixture(scope="package")
def sess(transit: AppTest):
    return transit.session_state


def test_default_date(transit: AppTest):
    assert transit.date_input(key="date2").value == date.today()


def test_sample_data(transit: AppTest, sess: SafeSessionState):
    transit.text_input(key="name1").set_value("sample")
    transit.date_input(key="date1").set_value(date(1976, 4, 20))
    transit.selectbox(key="hr1").set_value(18)
    transit.selectbox(key="min1").set_value(58)
    transit.selectbox(key="city1").set_value("Hong Kong - HK")

    transit.date_input(key="date2").set_value(date(2014, 4, 20))
    transit.selectbox(key="hr2").set_value(18)
    transit.selectbox(key="min2").set_value(48)
    transit.selectbox(key="city2").set_value("Taipei - TW")

    transit.run()

    assert sess["name1"] == "sample"
    assert sess["city1"] == "Hong Kong - HK"
    assert sess["date1"] == date(1976, 4, 20)
    assert sess["hr1"] == 18
    assert sess["min1"] == 58
    assert sess["city2"] == "Taipei - TW"
    assert sess["date2"] == date(2014, 4, 20)
    assert sess["hr2"] == 18
    assert sess["min2"] == 48


def test_change_orbs(transit: AppTest, sess: SafeSessionState):
    transit.button(key="transit_orbs").click().run()
    assert sess.conjunction == 2
    assert sess.opposition == 2
    assert sess.trine == 2
    assert sess.square == 2
    assert sess.sextile == 1


def test_change_displays(transit: AppTest, sess: SafeSessionState):
    transit.button(key="inner_display2").click().run()
    assert sess.sun2 == True
    assert sess.moon2 == True
    assert sess.mercury2 == True
    assert sess.asc_node2 == False
    assert sess.jupiter2 == False
    assert sess.pluto2 == False


def test_save(sess: SafeSessionState, transit_sample: str):
    # assert json.loads(archive_str(sess)) == json.loads(transit_sample)
    ...


def test_prev_button(transit: AppTest, sess: SafeSessionState):
    # press prev button
    transit.button(key="prev").click().run()
    assert sess.date1 == date(1976, 4, 20)
    assert sess.name2 == "transit"
    assert sess.date2 == date(2014, 4, 19)
