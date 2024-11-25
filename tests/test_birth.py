import json
from . import data1_sample
from archive import archive_str, import_data
from datetime import date
from io import BytesIO
from pytest import fixture
from streamlit.runtime.state.safe_session_state import SafeSessionState
from streamlit.testing.v1 import AppTest


@fixture(scope="package")
def birth():
    return AppTest.from_file("main.py").run()


@fixture(scope="package")
def sess(birth: AppTest):
    return birth.session_state


def test_default_name(birth: AppTest):
    assert birth.text_input(key="name1").value == ""


def test_default_date(birth: AppTest):
    assert birth.date_input(key="date1").value == date(2000, 1, 1)
    assert birth.selectbox(key="hr1").value == 13
    assert birth.selectbox(key="min1").value == 0


def test_default_city(birth: AppTest):
    assert birth.selectbox(key="city1").value is None


def test_sample_data(birth: AppTest, sess: SafeSessionState):
    birth.text_input(key="name1").set_value("sample")
    birth.date_input(key="date1").set_value(date(1976, 4, 20))
    birth.selectbox(key="hr1").set_value(18)
    birth.selectbox(key="min1").set_value(58)
    birth.selectbox(key="city1").set_value("Hong Kong")
    birth.run()
    assert sess["name1"] == "sample"
    assert sess["city1"] == "Hong Kong"
    assert sess["date1"] == date(1976, 4, 20)


def test_save(sess: SafeSessionState, data1_sample: str):
    assert json.loads(archive_str(sess)) == json.loads(data1_sample)


def test_orb(birth: AppTest, sess: SafeSessionState):
    assert sess.conjunction == 7
    birth.number_input(key="conjunction").increment().run()
    assert sess.conjunction == 8


def test_display_entities_change(birth: AppTest, sess: SafeSessionState):
    birth.toggle(key="asc_node1").set_value(False).run()
    assert sess.asc_node1 is False


def test_next_button(birth: AppTest, sess: SafeSessionState):
    birth.button(key="next").click().run()
    assert sess["name1"] == "sample"
    assert sess["city1"] == "Hong Kong"
    assert sess["date1"] == date(1976, 4, 21)


def test_stats_ui(birth: AppTest, sess: SafeSessionState):
    birth.toggle(key="show_stats").set_value(True).run()
    assert sess["name1"] == "sample"
    assert "Celestial Bodies (sample)" in birth.markdown[3].value


def test_change_options(birth: AppTest):
    birth.selectbox(key="house_sys").select("Whole_Sign")
    birth.run()
    assert "00°♋00" in birth.markdown[3].value


def test_change_time(birth: AppTest, sess: SafeSessionState):
    birth.selectbox(key="hr1").set_value(0).run()
    assert sess["hr1"] == 0
    birth.selectbox(key="min1").set_value(0).run()
    assert sess["min1"] == 0


def test_import(birth: AppTest, sess: SafeSessionState, data1_sample: str):
    import_data(BytesIO(data1_sample.encode()), sess)
    birth.run()
    assert json.loads(archive_str(sess)) == json.loads(data1_sample)
    assert sess.conjunction == 7
