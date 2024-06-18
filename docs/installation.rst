.. _installation:

Installation
================


Using pip
------------

    .. code-block:: shell

        pip install waybacktweets

From source
-------------

    Clone the repository:

    .. code-block:: shell

        git clone git@github.com:claromes/waybacktweets.git

    Change directory:

    .. code-block:: shell

        cd waybacktweets

    Install poetry, if you haven't already:

    .. code-block:: shell

        pip install poetry


    Install the dependencies:

    .. code-block:: shell

        poetry install

    Run the CLI:

    .. code-block:: shell

        poetry run waybacktweets [SUBCOMMANDS]

    Run the Streamlit App:

    .. code-block:: shell

        streamlit run app/app.py

    Build the docs:

    .. code-block:: shell

        cd docs

    .. code-block:: shell

        make clean html

`Read the Poetry CLI documentation <https://python-poetry.org/docs/cli/>`_.
