--------------------------
Get All Data
--------------------------

You can get the entire data with the code below.

    - ``YOUR_API_KEY`` stands for your Alta Data API key.
    - ``PRODUCT_CODE`` is a code created to use the Data Product with api. 

You can find the **product code** in the api section of the data product page.

.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(PRODUCT_CODE).load()



Get Data with Conditions
--------------------------

You can get data with using various conditions. 

The columns you can apply these filter operations to are limited to the **filtered columns**.

You can find the **filtered columns** in the data section of the data product page.

.. code:: python

    product_code = "co_10_jhucs_03"

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(product_code = product_code)\
            .equal(condition_column="province_state", condition_value="Montana")\
            .load()

