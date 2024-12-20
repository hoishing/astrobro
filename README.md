# AstroBro

> your astrology bro

## Usage

### Use Online on Streamlit Cloud

<https://astrobro.streamlit.app>

### Install PWA (Progressive Web App)

- visit: <https://hoishing.github.io/astrobro>
- Desktop:
    - Chrome: click `Install` button in the address bar
    - Safari: click `Share` button then choose `Add to Dock`
- Mobile: click `Share` button then choose `Add to Home Screen`

### Install and Run Locally with Python

```bash
# clone the repo
git clone https://github.com/hoishing/astrobro.git
cd astrobro

# install dependencies
pip install natal streamlit streamlit-shortcuts

# run the app
streamlit run main.py
```

## Road Map

- [x] Birth chart
- [x] Transit chart
- [x] Synastry chart
- deployment
    - [x] web app with [Streamlit] community cloud
    - [ ] local install with `pyinstaller`
    - [ ] mobile app
- [x] Natal chart in SVG with [natal]
- [x] Celestial bodies statistics with [natal]
- [x] date stepper
- options
    - [x] house system
    - [x] color theme
    - [x] toggle stats
    - [x] orbs
        - [x] clear / transit / default presets
    - [x] show / hide celestial bodies
        - [x] default / inner / planets presets
    - [ ] custom theme colors
- [ ] AI chart interpretation
- [ ] chat with AI
- [x] print chart and stats in PDF
- [ ] save charts in browser local storage
- [ ] import / export charts info and settings
- [ ] i18n
- [ ] custom components
    - [ ] settings dialog
    - [ ] screen size detection -> auto chart size

[streamlit]: https://streamlit.io
[natal]: https://github.com/hoishing/natal

## Need Help?

- [github issue]
- [x.com posts]
- [contact the author]

[contact the author]: https://hoishing.github.io
[github issue]: https://github.com/hoishing/astrobro/issues
[x.com posts]: https://x.com/hoishing
