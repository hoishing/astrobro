# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the Application
```bash
streamlit run main.py
```

### Package Management (use UV only)
```bash
# Add dependencies
uv add package_name

# Remove dependencies  
uv remove package_name

# Activate environment before running CLI tools
source .venv/bin/activate
```

### Testing
```bash
# Run tests (from project root)
pytest

# Run specific test file
pytest tests/test_birth.py

# Run with coverage
pytest --cov
```

### Code Quality
```bash
# Format and lint with ruff
ruff check .
ruff format .
```

## Architecture

### Core Structure
This is a Streamlit-based astrology application built around the `natal` library for chart generation. The app has a modular architecture:

- **main.py**: Application entry point, configures layout and coordinates UI components
- **ui.py**: Contains all UI components and form handlers (323 lines, largest module)
- **const.py**: Configuration constants, page settings, and UI styling
- **utils.py**: Helper functions for data processing (cities, datetime conversion)
- **archive.py**: Data serialization for save/load functionality using Pydantic models

### Data Flow
1. User inputs birth data via forms in `ui.py:data_form()`
2. Data is processed through `ui.py:data_obj()` to create `natal.Data` objects
3. Charts are generated via `natal.Chart` and rendered as SVG
4. Statistics are computed via `natal.Stats` and displayed as HTML

### Key Dependencies
- **natal**: Core astrology calculation library (charts, ephemeris, aspects)
- **streamlit**: Web framework for the UI
- **pandas**: City data management (cities.csv.gz)
- **pydantic**: Data validation and serialization
- **st-screenwidth-detector**: Dynamic chart sizing

### Session State Management
Streamlit session state stores:
- User input data (name1/2, city1/2, date1/2, hr1/2, min1/2)
- Configuration (house_sys, theme_type, orb settings)
- Display preferences (show_stats, celestial body visibility)

### Testing Strategy
Uses pytest with Streamlit's testing framework (`AppTest`). Tests cover:
- Default values and form interactions
- Data persistence and save/load functionality
- UI state changes and navigation
- Chart generation with different configurations

## Development Notes

### Code Style (from .cursor/rules/)
- Python 3.12+ required with full type hints
- Use modern type syntax: `list[int]`, `dict[str, int]`, `A | B`
- Single-line docstrings without parameter documentation
- `pathlib.Path` instead of `os.path`

### Key Patterns
- UI components return data tuples for form inputs
- Session state accessed via `sess = st.session_state` shorthand
- Heavy use of Streamlit columns for layout (`st.columns()`)
- Lambda functions for button callbacks with session state updates
- Cached city data loading with `@st.cache_resource`

### Chart Generation
Charts are dynamically sized based on screen width (min 650px) and rendered as SVG markup. The `natal` library handles all astronomical calculations, coordinate systems, and aspect computations.