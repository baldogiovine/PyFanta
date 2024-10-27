# PyFanta
<div align="center">
    <a href="<DOCS URL HERE>"><img src="assets/logo.png" alt="PyFanta" height="128px" width="128px"></a>
    <p align="center">
        <em>An API to scrape Fantacalcio data.</em>
    </p>
    <p align="center">
        <a href="https://github.com/baldogiovine/PyFanta/actions/workflows/ci.yml" target="_blank">
            <img src="https://github.com/baldogiovine/PyFanta/actions/workflows/ci.yml/badge.svg" alt="CI Pipeline status">
        </a>
        <a href="https://github.com/baldogiovine/PyFanta/releases" target="_blank">
            <img src="https://img.shields.io/github/v/release/baldogiovine/PyFanta?label=Latest%20Release" alt="Latest release">
        </a>
        <a href="https://github.com/baldogiovine/PyFanta" target="_blank">
            <img src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue" alt="Python version">
        </a>
        <!-- <a href="https://squidfunk.github.io/mkdocs-material/" target="_blank">
            <img src="https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white" alt="Docs built with Material for MkDocs">
        </a> -->
        <a href="https://github.com/astral-sh/ruff" target="_blank">
            <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
        </a>
    </p>
</div>


## Getting started

### Installation
```pip install -r requirements-dev.txt```

```uvicorn src.api.main:app --reload```

### TODO
- [x] fix malus (set it to 0 or null). for whatever reason a -1 mauls is set-up by
default.
- [x] check if it makes sense that all game days (from 1 to 38) are automatically
generated since the beginning. other attributes may not have as many values. some
players may have not joined the season since the first day. look if it is possible to
scrape the game-day value
- [x] for whatever reason bonus and malus automatically get 38 values. so cut them at
the correct number of game days
- [x] substitutioin_out is not working: it's taking values from substitution_in

### Quickstart
bla bla bla


## Credits

Author: [baldogiovine](https://github.com/baldogiovine)
