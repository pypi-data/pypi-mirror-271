# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.4.0 - 2024-05-02

### Added

- Add markdown rendering for post content. ([#11](https://todo.sr.ht/~loges/poaster/11))

### Changed

- Drop the generated summary based on text field.

## 1.3.0 - 2024-03-08

### Added

- Add initial web application. ([#8](https://todo.sr.ht/~loges/poaster/8))
- Add support for dotenv in pydantic settings.

### Changed

- Move service commands into a class to simplify API.
- Organize cli commands by domain.

### Fixed

- Fetch the secret key from settings not environment.

## 1.2.0 - 2024-03-05

### Added

- Make log level configurable in app settings. ([#5](https://todo.sr.ht/~loges/poaster/5))
- Add `post_versions` table for tracking post history. ([#6](https://todo.sr.ht/~loges/poaster/6))
- Expose ability to update posts from JSON API. ([#7](https://todo.sr.ht/~loges/poaster/7))
- Expose ability to delete posts from JSON API. ([#9](https://todo.sr.ht/~loges/poaster/9))

## 1.1.0 - 2024-02-13

### Added

- Add JSON API endpoints for handling bulletin posts. ([#2](https://todo.sr.ht/~loges/poaster/2))

### Fixed

- Constrain the value length of input credentials. ([#3](https://todo.sr.ht/~loges/poaster/3))

## 1.0.0 - 2024-02-12

### Added

- Add CLI for user management and running the application. ([#1](https://todo.sr.ht/~loges/poaster/1))
- Add JSON API endpoints for authenticating users with JWT.
