--------------------------
ALTADATA Python Library
--------------------------

ALTADATA Python library provides convenient access to the ALTADATA API from
applications written in the Python language.

.. contents:: Overview
    :depth: 2

Installation
=============

.. code-block::

    pip install altadata


Retrieving Data
==================

You can get the entire data with the code below. This function returns List of dict by default.

.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(PRODUCT_CODE).load()


If **dataframe_functionality** parameter is True function returns pandas dataframe.

``Note:`` This functionality requires `pandas <https://github.com/pandas-dev/pandas>`_ (v0.21 or above) to work.

.. code:: python

    client = AltaDataAPI(api_key=YOUR_API_KEY, dataframe_functionality=True)
    data = client.get_data(PRODUCT_CODE).load()


Documentation
=============

Read the documentation online at `altadata-python.rtfd.io <https://altadata-python.rtfd.io>`_

Optionally, build documentation from the ``docs/`` folder

.. code-block::

    pip install sphinx
    cd docs
    make html


License
=============

altadata-python is under MIT license. See the `LICENSE <LICENSE>`_ file for more info.
