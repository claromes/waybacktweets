import datetime

from pallets_sphinx_themes import ProjectLink, get_version

project = "Wayback Tweets"
release, version = get_version("waybacktweets")
rst_epilog = f".. |release| replace:: v{release}"
copyright = f"2023 - {datetime.datetime.now().year}, Claromes · Icon by The Doodle Library · Title font by Google, licensed under the Open Font License · Release: v{release}"  # noqa: E501
author = "Claromes"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "pallets_sphinx_themes",
    "sphinxcontrib.mermaid",
    "sphinx_new_tab_link",
    "sphinx_click.ext",
    "sphinx_autodoc_typehints",
]

templates_path = ["docs/_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------

html_theme = "flask"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/waybacktweets/"),
        ProjectLink("Source Code", "https://github.com/claromes/waybacktweets/"),
        ProjectLink(
            "Issue Tracker", "https://github.com/claromes/waybacktweets/issues/"
        ),
        ProjectLink("Mastodon", "https://ruby.social/@claromes"),
        ProjectLink("Bluesky", "https://bsky.app/profile/claromes.com"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
html_favicon = "../assets/parthenon.png"
html_logo = "../assets/parthenon.png"
html_title = f"Wayback Tweets Documentation ({version})"
html_show_sourcelink = False
