--------------------------
List Subscription
--------------------------

You can get your subscription info with the code below. :func:`~altadata.AltaDataAPI.list_subscription` returns **list of dict** by default. 

Firstly import library with the code below.

.. code:: python

    from altadata.altadata import *


.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    product_list = client.list_subscription()


If **dataframe_functionality** parameter is True :func:`~altadata.AltaDataAPI.list_subscription` returns **pandas dataframe**.

``Note:`` This functionality requires `pandas <https://github.com/pandas-dev/pandas>`_ (v0.21 or above) to work.

.. code:: python

    client = AltaDataAPI(api_key=YOUR_API_KEY, dataframe_functionality=True)
    product_list = client.list_subscription()
