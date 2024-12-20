# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- Add atrribute `player_of_the_match` to `v1/matches-stats` endpoint. From YEAR="2024-25" a new bonus has been added. This bonus is "Player of the match". Based on the league settings, this add a bonus of "+1".

### Fixed
- There is a known bug related to players matches information. Data coming out of `v1/matches-stats` endpoint are not outputted in the desired format. Which should be a format that can potentially allow to easily take these data as input in a time series forecasting model.

## [0.1.0] - 2024-11-24

### Added
- API endpoint to scrape information about all players performance in all matches in a specific season. | `v1/matches-stats` endpoint
- API endpoint to scrape overall information of outfield players (attackers, midfilders, and defenders) in a season. | `v1/player-summary-stats/outfield` endpoint
- API endpoint to scrape overall information of goalkeepers in a season. | `v1/player-summary-stats/goalkeper` endpoint

[0.1.0]: https://github.com/baldogiovine/PyFanta/releases/tag/v0.1.0
