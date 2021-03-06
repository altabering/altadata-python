--------------------------
ALTADATA Python Client
--------------------------

.. image:: https://github.com/altabering/altadata-python/workflows/build/badge.svg
    :target: https://github.com/altabering/altadata-python/actions

.. image:: https://badge.fury.io/py/altadata.svg
    :target: https://pypi.org/project/altadata

.. image:: https://anaconda.org/altadata/altadata/badges/version.svg
    :target: https://anaconda.org/altadata/altadata

|

`ALTADATA <https://www.altadata.io>`_ is a Curated Data Marketplace. This Python library provides convenient access to the ALTADATA API from applications written in the Python language. With this Python library, developers can build applications around the ALTADATA API without having to deal with accessing and managing requests and responses.

.. contents:: **Overview**
    :depth: 2

Installation
==================

You can install the package via `pip <https://pip.pypa.io/en/stable/>`_

.. code-block::

    pip install altadata

You can install the package via `conda <https://docs.conda.io/en/latest/>`_

.. code-block::

    conda install altadata::altadata


Retrieving Data
==================

You can get the entire data with the code below. This function returns List of dict by default.

.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(PRODUCT_CODE).load()


We currently have pandas dataframe support in the library. Users can optionally retrieve their datasets as pandas dataframe.
If **dataframe_functionality** parameter is True function returns pandas dataframe.

``Note:`` This functionality requires `pandas <https://github.com/pandas-dev/pandas>`_ (v0.25.3 or above) to work.

.. code:: python

    client = AltaDataAPI(api_key=YOUR_API_KEY, dataframe_functionality=True)
    data = client.get_data(PRODUCT_CODE).load()

You can get data with using various conditions. 

.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(PRODUCT_CODE)\
            .equal(condition_column=COLUMN_NAME, condition_value=CONDITION_VALUE)\
            .sort(order_column=COLUMN_NAME, order_method="desc")\
            .load()


Documentation
==================

Read the documentation online at `altadata-python.rtfd.io <https://altadata-python.rtfd.io>`_

Optionally, build documentation from the ``docs/`` folder

.. code-block::

    pip install sphinx
    cd docs
    make html


License
==================

altadata-python is under MIT license. See the `LICENSE <LICENSE>`_ file for more info.
