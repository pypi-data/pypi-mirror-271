from typing import Iterable, TypedDict

import haitch as H
import mistletoe as md

from . import config


def page(content: H.SupportsHtml, *, title: str, username: str = "") -> H.Element:
    """Base HTML container for building web pages."""
    return H.html5(
        content=H.fragment(
            navbar(username),
            content,
            footer(),
        ),
        page_title=f"{title} - {config.settings.title}",
        language_code="en",
        body_classes="flex-wrapper",
        links=(
            H.link(rel="stylesheet", href="/static/normalize.css"),
            H.link(rel="stylesheet", href="/static/concrete.css"),
            H.link(rel="stylesheet", href="/static/app.css"),
        ),
    )


def not_found_page(*, username: str) -> H.Element:
    """Not found 404 page."""
    content = message("Page not found.", variant="warning")
    return page(content, title="404 - Not found", username=username)


def unauthorized_page() -> H.Element:
    """Unauthorized 401 page."""
    content = message("Unauthorized: please login.", variant="danger")
    return page(content, title="401 - Unauthorized")


class LinkProp(TypedDict):
    """Anchor link prop."""

    name: str
    href: str
    show: bool


def links(props: Iterable[LinkProp]) -> H.Element:
    """List of URL links."""
    style = "padding-right: 1.7rem;"
    return H.span(
        H.a(href=prop["href"], style=style)(prop["name"])
        for prop in props
        if prop["show"]
    )


def logo() -> H.Element:
    """Logo component that links to home."""
    logo_style = (
        "padding-right: 3rem;"
        "text-decoration: none;"
        f"color: {config.settings.get_color(variant='primary')};"
        "font-family: monospace;"
    )
    return H.a(href="/", style=logo_style)(config.settings.title)


def navbar(username: str) -> H.Element:
    """Navbar component."""
    nav_style = "flex-direction: row; padding: 2rem 0;"
    nav_links: Iterable[LinkProp] = [
        {"name": "+add", "href": "/posts/new", "show": username != ""},
        {"name": "logout", "href": "/logout", "show": username != ""},
        {"name": "login", "href": "/login", "show": not username},
    ]
    return H.header(
        H.nav(style=nav_style)(
            logo(),
            links(nav_links),
        )
    )


def footer() -> H.Element:
    """Footer component."""
    return H.footer(
        H.small("poaster "),
        H.a(href="https://sr.ht/~loges/poaster/")(H.small("[source]")),
    )


def message(text: str, variant: config.ColorVariant) -> H.Element:
    """Message component for with consistent styling based on variant provided."""
    color = config.settings.get_color(variant)
    style = (
        "padding: 2rem;"
        f"border-left: thick solid {color};"
        f"background: {color}13;"
        "padding-left: 1.2em;"
    )
    return H.p(style=style)(text)


def markdown_to_html(text: str) -> H.Element:
    """Render markdown text to HTML."""
    with md.HtmlRenderer() as renderer:
        rendered_html = renderer.render(md.Document(text))
    return H.unsafe(rendered_html)
