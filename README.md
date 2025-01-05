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
        <!-- <a href="https://github.com/baldogiovine/PyFanta/releases" target="_blank">
            <img src="https://img.shields.io/github/v/release/baldogiovine/PyFanta?label=Latest%20Release" alt="Latest release">
        </a> -->
        <a href="https://github.com/baldogiovine/PyFanta" target="_blank">
            <img src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue" alt="Python version">
        </a>
        <!-- <a href="https://squidfunk.github.io/mkdocs-material/" target="_blank">
            <img src="https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white" alt="Docs built with Material for MkDocs">
        </a> -->
        <a href="https://github.com/astral-sh/ruff" target="_blank">
            <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
        </a>
        <a href="http://www.mypy-lang.org/" target="_blank">
            <img src="https://img.shields.io/badge/mypy-checked-blue" alt="mypy">
        </a>
    </p>
</div>

## What is it?
**pyFanta** is a scraper wrapped in a [FastAPI](https://github.com/fastapi/fastapi) application that helps you extract data from [Leghe Fantacalcio](https://www.fantacalcio.it).

Its purpose is to assist you with your fantacalcio auctions and repair auctions, offering support in choosing your weekly lineup.

## Disclaimer
This tool is intended solely and exclusively for personal, educational, recreational, non-commercial, and non-profit uses and purposes.

Please be considerate with the rate at which you send requests to the website. Excessive or rapid requests can place unnecessary strain on the website's servers, potentially leading to service disruptions for other users or triggering anti-scraping measures.

Users are responsible for ensuring that their use of this tool complies with all applicable laws and the terms of service of the [website](https://www.fantacalcio.it) they interact with. The author does not condone or support any misuse of this tool.

Before using the Code, please carefully read the [`pyFanta Licencse`](LICENSE)

## Table of Contents
- [PyFanta](#pyfanta)
  - [What is it?](#what-is-it)
  - [Disclaimer](#disclaimer)
  - [Table of Contents](#table-of-contents)
  - [Currently implemented features](#currently-implemented-features)
  - [Installation](#installation)
  - [Quickstart](#quickstart)
  - [Running with Docker](#running-with-docker)
  - [API documentation](#api-documentation)
    - [Requests examples](#requests-examples)
  - [Releases](#releases)
  - [License](#license)
  - [Support](#support)
  - [Credits](#credits)

## Currently implemented features
Here is a list of currently implemented features:
- **Player Match Statistics**: API endpoint to scrape performance data of all players in all matches for a specific season. | Endpoint: `/v1/matches-stats`
- **Outfield Player Summary**: API endpoint to scrape overall statistics of outfield players (attackers, midfielders, defenders) in a season. | Endpoint: `/v1/player-summary-stats/outfield`
- **Goalkeeper Summary**: API endpoint to scrape overall statistics of goalkeepers in a season. | Endpoint: `/v1/player-summary-stats/goalkeeper`

Important notes:
- Currently only `Serie A` league is implemented.
- Once started up, the API will be locally hosted on your machine. Currently there is no implementation to host the API on a port other then `8000`.

[Back to Table of Contents](#table-of-contents)

## Installation
To make use of **pyFanta** API, follow the indicated steps to clone the repository and the install the required packages.

Clone the repository:
```
git clone https://github.com/baldogiovine/PyFanta.git
```

Navigate to the project directory:
```
cd PyFanta
```

Create a virtual environment (optional):
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install required packages:
```
pip install -r requirements.txt
```

[Back to Table of Contents](#table-of-contents)

## Quickstart
To start up **pyFanta** API, follow the indicated steps to start the FastAPI server:

Navigate to the project directory:
```
cd PyFanta
```

Start the FastAPI server:
```
uvicorn src.api.main:app
```

```uvicorn src.api.main:app --reload``` can be used instead of ```uvicorn src.api.main:app``` to enable auto-reloading of the server when code changes.

Running ```python3 -m src.client``` will execute the client code and download in the `data` folder all Serie A mathces, outfield players, and goalpeers information for season `2024-25` both in `json` and `csv` format.

To scrape data about other seasons access `src.client.py` and modify the value of the `YEAR` constant from `2024-25` to, for example, `2023-24`.

For more details on current issues, please refer to the [Known Bugs](#known-bugs) section.

[Back to Table of Contents](#table-of-contents)

## Running with Docker
A packaged version of the **pyFanta** API is offered through a [Docker](https://www.docker.com/) image. It's possible to interact with the packaged version of the **pyFanta** API in various ways. For example, you can create a Docker container from the image and interact with the API using tools like [Postman](https://www.postman.com/downloads/).

To build the Docker image and create a container from it, follow the below instructions.

Navigate to the project directory:
```
cd PyFanta
```

Build the Docker image using the [Dockerfile](Dockerfile) in the [repository](https://github.com/baldogiovine/PyFanta):
```
docker build -t pyfanta .
```

Create and run the container:
```
docker run -d -p 8000:8000 pyfanta
```

Once the container is running, you can access the **pyFanta** API at [http://localhost:8000](http://localhost:8000). To explore the API documentation and test endpoints, visit [http://localhost:8000/docs](http://localhost:8000/docs).

[Back to Table of Contents](#table-of-contents)

## API documentation
The **pyFanta** API is organized into distinct routers, as illustrated in the diagram below:

```mermaid
graph TD;
  A[pyFanta API] --> B[Links Router];
  A --> C[Matches Router];
  A --> D[Players Router];

  B --> E[GetPlayersLinks Endpoint];
  C --> F[GetMatchesStats Endpoint];
  D --> G[GetOutfieldPlayerSummaryStats Endpoint];
  D --> H[GetGoalkeeperSummaryStats Endpoint];
```

The `GetPlayersLinks endpoint` accepts a season identifier (e.g. `YEAR="2024-25"`, `YEAR="2023-24"`) and retrieves all corresponding `PlayerLink` objects for that season. This `PlayerLink` structure, which is defined as the below [Pydantic](https://docs.pydantic.dev/latest/) model, serves as the basic input for all other endpoints.

```
class PlayerLink(BaseModel):
    name: str
    link: str
```

<div align="center">

```mermaid
classDiagram
    class PlayerLink{
        +String name
        +String link
    }
```

</div>

Once the [API is up and runing](#quickstart), you can access the following link to visualize the API documentation:

```https://127.0.0.1:8000/docs```

This will open the interactive API documentation generated by [Swagger UI](https://swagger.io/tools/swagger-ui/), allowing you to explore available endpoints, examine request/response formats, and test queries directly from your browser.

[Back to Table of Contents](#table-of-contents)

### Requests examples
Once the API is up and running, either through [Uvicorn](#quickstart) or [Docker](#running-with-docker), you can start making requests to the various endpoints.

In this example, we will use [Postman](https://www.postman.com/downloads/) to interact with the API running inside a Docker container. The following image shows the Postman environment variables used for these requests:

<div align="center">

![Postman environment variables](assets/example_postman_variables.png)

</div>

As explained in the [API Documentation](#api-documentation) section, the first step is to obtain the `PlayerLink` objects. The image below demonstrates a `GET` request to the `GetPlayersLinks` endpoint:

<div align="center">

![Postman GET request on the GetPlayersLinks endpoint](assets/example_postman_player_links.png)

</div>

Once you have a `PlayerLink` object, you can use it to query other endpoints. For example, you can send a `POST` request to the `GetOutfieldPlayerSummaryStats` endpoint as shown below:

<div align="center">

![Postman POST request on the GetOutfieldPlayerSummaryStats endpoint](assets/example_postman_outfield_players.png)

</div>

[Back to Table of Contents](#table-of-contents)

## Releases
Check out [CHANGELOG.md](CHANGELOG.md) to stay updated on new releases, features, and bug fixes!

[Back to Table of Contents](#table-of-contents)

## License
This project is licensed under the **PyFanta License**. See the [LICENSE](LICENSE) file for details.

[Back to Table of Contents](#table-of-contents)

## Support

If you encounter any issues or have questions, please open an [issue](https://github.com/baldogiovine/PyFanta/issues) on GitHub.

[Back to Table of Contents](#table-of-contents)

## Credits

**Author:**
- [baldogiovine](https://github.com/baldogiovine)

**Acknowledgments**:
- [Leghe Fantacalcio](https://www.fantacalcio.it) for the data source.

[Back to Table of Contents](#table-of-contents)
