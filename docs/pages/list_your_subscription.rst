--------------------------
List Subscription
--------------------------

You can get your subscription info with the code below.

.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    product_list = client.list_subscription()


This function returns pandas dataframe by default. If **return_as_dataframe** parameter is set to False then List of dict is returned.
