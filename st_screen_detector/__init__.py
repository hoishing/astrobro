import streamlit.components.v1 as components

__all__ = ["screen_detector"]

RELEASE = True

name = "screen_detector"

if RELEASE:
    from pathlib import Path

    parent_dir = Path(__file__).parent
    build_dir = parent_dir / "frontend" / "dist"
    opt = {"path": str(build_dir)}
else:
    opt = {"url": "http://localhost:5173"}

_component_func = components.declare_component(name, **opt)


def screen_detector(key=name):
    component_value = _component_func(key=key, default=0)
    return component_value
