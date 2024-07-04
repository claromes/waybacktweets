Installation
================

**It is compatible with Python versions 3.10 and above.**

Using pip
------------

    .. code-block:: shell

        pip install waybacktweets

Using Poetry
------------

    .. code-block:: shell

        poetry add waybacktweets

.. _installation_from_source:

From source
-------------

    **Clone the repository:**

    .. code-block:: shell

        git clone git@github.com:claromes/waybacktweets.git

    **Change directory:**

    .. code-block:: shell

        cd waybacktweets

    **Install Poetry, if you haven't already:**

    .. code-block:: shell

        pip install poetry


    **Install the dependencies:**

    .. code-block:: shell

        poetry install

    **Install the pre-commit:**

    .. code-block:: shell

        poetry run pre-commit install

    **Run the CLI:**

    .. code-block:: shell

        poetry run waybacktweets [SUBCOMMANDS]

    **Starts a new shell and activates the virtual environment:**

    .. code-block:: shell

        poetry shell

    **Run the Streamlit App:**

    .. code-block:: shell

        streamlit run app/app.py

    **Build the docs:**

    .. code-block:: shell

        cd docs

    .. code-block:: shell

        make clean html

`Read the Poetry CLI documentation <https://python-poetry.org/docs/cli/>`_.
