"""constants"""

from natal import Data
from natal.config import Display
from pathlib import Path

SOURCE_CODE = """\
![github](https://api.iconify.design/bi/github.svg?color=%236FD886&width=20) &nbsp;
[source code](https://github.com/hoishing/astrobro)
"""

ABOUT = f"💫 &nbsp;AstroBro :&nbsp; your pocket astrologer\n\n{SOURCE_CODE}"

PAGE_CONFIG = dict(
    page_title="AstroBro",
    page_icon="💫",
    menu_items={
        "About": ABOUT,
        "Get help": "https://github.com/hoishing/astrobro/issues",
    },
)

CITY_ASCII = Data.cities.iloc[:, 0]
BODIES = Display().model_fields.keys()
STYLE = f"<style>{Path("style.css").read_text()}</style>"
LOGO = "static/astrobro-logo.png"
