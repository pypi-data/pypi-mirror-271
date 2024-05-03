# poaster

---

[![builds.sr.ht status](https://builds.sr.ht/~loges/poaster.svg)](https://builds.sr.ht/~loges/poaster?)
[![PyPI - Version](https://img.shields.io/pypi/v/poaster.svg)](https://pypi.org/project/poaster)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

> Minimal, libre bulletin board for posts.

You can see a simple demo of poaster [here](https://poaster.loganconnolly.com).

## Features

- Display bulletin posts to all users.
- Create, update, and delete posts as authenticated user.
- Manage posts through web app and JSON API.
- Offer CLI for managing users and app state.
- Expose configuration options through environment variables.

## Roadmap

- Refined access control (admin, members, public).
- Add markdown support for post content.

## Quickstart

Install package:

```console
pip install poaster
```

Initialize application:

```console
poaster init
```

Add a user:

```console
poaster users add
```

Launch application server:

```console
poaster run
```

## Configuration

You can configure parts of the application in the shell environment. Here's an example `.env`:

```shell
# Logging
LOG_LEVEL="info"

# Database
DB_PATH="/./poaster.db"

# Security
SECRET_KEY="<generated-when-initializing-app>"
SECRET_KEY_N_BYTES=32
ALGORITHM="HS256"

# Theming
TITLE="poaster"
COLOR_DANGER="#FF595E"
COLOR_INFO="#1982C4"
COLOR_PRIMARY="#6A4C93"
COLOR_SUCCESS="#8AC926"
COLOR_WARINING="#FFCA3A"
```

## Development

The easiest way to develop locally with `poaster` is to use [hatch](https://hatch.pypa.io/latest/). With `hatch`, you will have access to important helper scripts for running locally, linting, type-checks, testing, etc.

### Testing

Lint and check types with:

```console
hatch run types:check
```

Run test suite and report coverage with:

```console
hatch run cov
```

### Database Management

To upgrade the local database to latest schema, run:

```console
hatch run db:upgrade
```

Now that the tables are created, you can add fixtures:

```console
hatch run db:fixtures
```

If you add or update a table, you can generate a migration script by running:

```console
hatch run db:migration
```

If the migration script wasn't generated, check to see if you imported the model to [env.py](src/poaster/migrations/env.py).

### Local Server

Run the application server locally with:

```console
hatch run dev
```

The server should reload on changes to the source code.

## License

`poaster` is distributed under the terms of the [AGPLv3](https://spdx.org/licenses/AGPL-3.0-or-later.html) license.
