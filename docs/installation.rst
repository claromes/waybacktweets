Installation
================

**It is compatible with Python versions 3.10 and above.**

Using pipx
------------

    .. code-block:: shell

        pipx install waybacktweets

Using pip
------------

    .. code-block:: shell

        pip3 install waybacktweets

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

        pip3 install poetry

    **Install the dependencies:**

    .. code-block:: shell

        poetry install

    **Install the pre-commit:**

    .. code-block:: shell

        poetry run pre-commit install

    **Run the CLI:**

    .. code-block:: shell

        poetry run waybacktweets [OPTIONS] USERNAME

    **Run the Streamlit App:**

    - Starts a new shell and activates the virtual environment:

        .. code-block:: shell

            poetry shell

    - Run the Streamlit:

        .. code-block:: shell

            streamlit run app/app.py

    **Build the docs:**

    .. code-block:: shell

        cd docs

    .. code-block:: shell

        make clean html
