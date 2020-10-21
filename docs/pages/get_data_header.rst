--------------------------
Get Header
--------------------------

You can get your data header with the code below.

.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    header = client.get_get_header(PRODUCT_CODE).load()


This function returns list.
