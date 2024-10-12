# AstroBro

> your astrologer bro

## Usage

- use on streamlit cloud:

<https://astrobro.streamlit.app>

- run in browser with WASM using [StLite]

<https://hoishing.github.io/astrobro>

- install locally with python

```bash
# install dependencies
pip install natal streamlit streamlit-shortcuts libsass

# run the app
streamlit run main.py
```

# Road Map

- [x] Birth chart
- [x] Transit chart
- [x] Synastry chart
- web interface with [Streamlit]
    - [x] community server hosted
    - [ ] client side only with WASM using [StLite]
- [x] Natal chart in SVG with [natal]
- [x] Celestial bodies statistics with [natal]
- [x] date stepper
- options
    - [x] house system
    - [x] color theme
    - [x] orbs
    - [ ] show / hide celestial bodies
    - [ ] custom theme colors
    - [ ] save options in browser local storage
    - [ ] separate options for different kinds of charts
- [ ] Birth chart interpretation
- [ ] Transit chart interpretation
- [ ] Synastry chart interpretation
- [ ] print chart and stats in PDF
- [ ] chat with AI
- [ ] mobile app
- [ ] save charts in browser local storage
- [ ] import / export charts info and settings

[streamlit]: https://streamlit.io
[stlite]: https://github.com/whitphx/stlite
[natal]: https://github.com/hoishing/natal
