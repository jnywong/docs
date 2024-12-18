# -- Project information -----------------------------------------------------

project = "Service Guide"
copyright = "2022"
author = "2i2c"
version = "0.1"
main_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx.ext.intersphinx",
    "sphinxext.rediraffe",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md", ".github", ".nox", "CONTRIBUTING.md"]

myst_enable_extensions = ["colon_fence", "deflist", "linkify"]
myst_heading_anchors = 3

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_2i2c_theme"
html_title = "Hub Service Guide"
html_copy_source = True
html_sourcelink_suffix = ""

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "repository_url": "https://github.com/2i2c-org/docs",
    "repository_branch": "main",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "show_toc_level": 2,
}

intersphinx_mapping = {
    "tc": ('https://team-compass.2i2c.org', None),
    "infra": ('https://infrastructure.2i2c.org', None),
    "jb": ('https://jupyterbook.org/en/stable/', None),
    "z2jh": ('https://z2jh.jupyter.org/en/latest', None),
}

rediraffe_redirects = {
    # Added around 2022-09
    "about/overview.md": "about/service/index.md",
    "about/pricing/index.md": "about/service/options.md",

    # Added 2022-11-29
    "about/service/roles.md": "about/service/shared-responsibility.md",
    "about/service/team.md": "about/service/shared-responsibility.md",

}

# Disable linkcheck for anchors because it throws false errors for any JS anchors
linkcheck_anchors = False
linkcheck_ignore = [
    "https://openstoragenetwork.org*",  # It incorrectly fails with `Max retries exceeded with url`
    "https://docs.github.com*",  # Because docs.github.com returns 403 Forbidden errors
]

# Embed a contact form Freshdesk widget to collect support tickets with
widget_embed_code = """
// This is the function to open the widget code
function openWidget() {
    FreshworksWidget('open');
}

// FreshWorks widget loading code
window.fwSettings={
    'widget_id':80000009162
};
!function(){if("function"!=typeof window.FreshworksWidget){var n=function(){n.q.push(arguments)};n.q=[],window.FreshworksWidget=n}}() 
"""

def setup(app):
    app.add_css_file("custom.css")
    app.add_crossref_type("team", "team")
    app.add_crossref_type("role", "role")

    # Add the JS code for our FreshDesk support widget
    # ref: https://support.freshdesk.com/en/support/solutions/articles/239273-setting-up-your-help-widget
    # ref: https://support.freshdesk.com/en/support/solutions/articles/50000001015-launching-the-widget-when-a-button-is-clicked
    app.add_js_file(None, body=widget_embed_code)
    app.add_js_file("https://euc-widget.freshworks.com/widgets/80000009162.js", **{"async": "", "defer": ""})

# -- Custom scripts -------------------------------------------------

# Generate the feature table
import subprocess
from pathlib import Path
build_assets = Path("build_assets")
build_assets.mkdir(exist_ok=True)
subprocess.run(["python", "feature-table.py"], cwd="scripts")

# Download figures we keep in Google Drive
from requests import get
figures = {
    "https://drive.google.com/uc?export=download&id=1Mr51-s3D_KHPsAuTXbczaQ7mlPZUs9gm": "collaborative_learning_hub.png",
    "https://drive.google.com/uc?export=download&id=16r5xE7SguunLfMh5LhSynSUfjb7IXs_n": "shared_responsibility_diagram.png",
    "https://drive.google.com/uc?export=download&id=1gWAIQVKcB-uxuJsBHqlDlRTq88oki1zn": "scalable_research_hub.png",
}
for url, filename in figures.items():
    path_image = Path(__file__).parent / "images" / filename
    if not path_image.exists():
        print(f"Downloading {filename}...")
        resp = get(url)
        path_image.write_bytes(resp.content)
    else:
        print(f"Diagram image exists, delete this file to re-download: {path_image}")

# -- Set canonical custom domain via html_baseurl -----------
# -- See https://github.com/2i2c-org/infrastructure/issues/4629
import os

html_context = {}

# Set canonical URL from the Read the Docs Domain
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    html_context["READTHEDOCS"] = True
