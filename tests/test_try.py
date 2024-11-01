from pytest import fixture
from streamlit.runtime.state.safe_session_state import SafeSessionState
from streamlit.testing.v1 import AppTest


# @fixture(scope="package")
# def app():
#     return AppTest.from_file("try.py", default_timeout=10000).run()


# def test_app(app: AppTest):
#     app.number_input(key="conjunction").increment().run()
