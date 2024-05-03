from pathlib import Path

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

import poaster.access.api
import poaster.access.web
import poaster.bulletin.api
import poaster.bulletin.web
from poaster.__about__ import __version__
from poaster.core import http_exceptions


def get_app() -> FastAPI:
    """Build and configure application server."""

    # main web application
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    # mount static files
    static_directory = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=static_directory), name="static")

    # include web endpoints
    app.include_router(poaster.access.web.router)
    app.include_router(poaster.bulletin.web.router)

    # exception handling
    app.add_exception_handler(
        status.HTTP_403_FORBIDDEN, http_exceptions.handle_forbidden
    )
    app.add_exception_handler(
        status.HTTP_404_NOT_FOUND, http_exceptions.handle_not_found
    )
    app.add_exception_handler(
        RequestValidationError, http_exceptions.handle_validation_error
    )

    # json api
    api = FastAPI(
        title="poaster API",
        version=__version__,
        summary="Minimal, libre bulletin board for posts.",
        license_info={
            "name": "GNU Affero General Public License (AGPL)",
            "url": "https://www.gnu.org/licenses/agpl-3.0.html",
        },
    )

    # include api endpoints
    api.include_router(poaster.access.api.router)
    api.include_router(poaster.bulletin.api.router)

    # mount api app to web app
    app.mount("/api", api)

    return app


app = get_app()
