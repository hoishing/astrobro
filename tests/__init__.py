from pytest import fixture


@fixture(scope="module")
def data1_sample():
    return """
        {
            "name1": "sample",
            "city1": "Hong Kong - HK",
            "dt1": "1976-04-20T18:58:00",
            "name2": "transit",
            "city2": null,
            "dt2": null,
            "house_sys": "Placidus",
            "theme_type": "dark",
            "orb": {
                "conjunction": 7,
                "opposition": 6,
                "trine": 6,
                "square": 6,
                "sextile": 5,
                "quincunx": 0
            },
            "display1": {
                "sun": true,
                "moon": true,
                "mercury": true,
                "venus": true,
                "mars": true,
                "jupiter": true,
                "saturn": true,
                "uranus": true,
                "neptune": true,
                "pluto": true,
                "asc_node": true,
                "chiron": false,
                "ceres": false,
                "pallas": false,
                "juno": false,
                "vesta": false,
                "asc": true,
                "ic": false,
                "dsc": false,
                "mc": true
            },
            "display2": {
                "sun": true,
                "moon": true,
                "mercury": true,
                "venus": true,
                "mars": true,
                "jupiter": true,
                "saturn": true,
                "uranus": true,
                "neptune": true,
                "pluto": true,
                "asc_node": true,
                "chiron": false,
                "ceres": false,
                "pallas": false,
                "juno": false,
                "vesta": false,
                "asc": true,
                "ic": false,
                "dsc": false,
                "mc": true
            }
        }
    """


@fixture(scope="module")
def transit_sample():
    return """
        {
            "name1": "sample",
            "city1": "Hong Kong - HK",
            "dt1": "1976-04-20T18:58:00",
            "name2": "transit",
            "city2": "Taipei - TW",
            "dt2": "2014-04-20T18:48:00",
            "house_sys": "Placidus",
            "theme_type": "dark",
            "orb": {
                "conjunction": 2,
                "opposition": 2,
                "trine": 2,
                "square": 2,
                "sextile": 1,
                "quincunx": 0
            },
            "display1": {
                "sun": true,
                "moon": true,
                "mercury": true,
                "venus": true,
                "mars": true,
                "jupiter": true,
                "saturn": true,
                "uranus": true,
                "neptune": true,
                "pluto": true,
                "asc_node": true,
                "chiron": false,
                "ceres": false,
                "pallas": false,
                "juno": false,
                "vesta": false,
                "asc": true,
                "ic": false,
                "dsc": false,
                "mc": true
            },
            "display2": {
                "sun": true,
                "moon": true,
                "mercury": true,
                "venus": true,
                "mars": true,
                "jupiter": false,
                "saturn": false,
                "uranus": false,
                "neptune": false,
                "pluto": false,
                "asc_node": false,
                "chiron": false,
                "ceres": false,
                "pallas": false,
                "juno": false,
                "vesta": false,
                "asc": true,
                "ic": false,
                "dsc": false,
                "mc": false
            }
        }
    """
