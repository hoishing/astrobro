import streamlit as st


page_config = dict(
    page_title="AstroBro",
    page_icon="💫",
    menu_items={
        "About": "AstroBro is a your pocket astrologer",
        "Get help": "https://github.com/hoishing/astrobro/issues",
    },
)


def header(title: str):
    st.markdown(
        """
        ### :dizzy: &nbsp; AstroBro

        > your pocket astrologer

        ![github](https://api.iconify.design/bi/github.svg?color=%236FD886&width=20) &nbsp;
        [source code](https://github.com/hoishing/astrobro)
        """
    )
    st.write("")
    st.write(f"#### {title}")
