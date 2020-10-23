--------------------------
Get Data
--------------------------

    - ``YOUR_API_KEY`` stands for your Alta Data API key.
    - ``PRODUCT_CODE`` is a code created to use the Data Product with API. 

You can find the **product code** in the api section of the data product page.


Get All Data
--------------------------

You can get the entire data with the code below. This function returns List of dict by default.

.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(PRODUCT_CODE).load()


If **dataframe_functionality** parameter is True returns pandas dataframe.

``Note:`` This functionality requires `pandas <https://github.com/pandas-dev/pandas>`_ (v0.14 or above) to work.

.. code:: python

    client = AltaDataAPI(api_key=YOUR_API_KEY, dataframe_functionality=True)
    data = client.get_data(PRODUCT_CODE).load()


Get Data with Conditions
--------------------------

You can get data with using various conditions. 

The columns you can apply these filter operations to are limited to the **filtered columns**.

You can find the **filtered columns** in the data section of the data product page.


equal condition
^^^^^^^^^^^^^^^^^^

.. code:: python

    product_code = "co_10_jhucs_03"

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(product_code = product_code)\
            .equal(condition_column="province_state", condition_value="Montana")\
            .load()


in condition
^^^^^^^^^^^^^^^^^^

.. code:: python

    product_code = "co_10_jhucs_03"

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(product_code)\
            .condition_in(condition_column="province_state", condition_value=["Montana", "Utah"])\
            .load()


not in condition
^^^^^^^^^^^^^^^^^^

.. code:: python

    product_code = "co_10_jhucs_03"

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(product_code)\
            .condition_not_in(condition_column="province_state", condition_value=["Montana", "Utah"])\
            .load()


sort operation
^^^^^^^^^^^^^^^^^^

    You can sort data based on a specific column and method.

.. code:: python

    product_code = "co_10_jhucs_03"

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(product_code)\
            .sort(order_column="mortality_rate", order_method="desc")\
            .load()


select specific columns
^^^^^^^^^^^^^^^^^^^^^^^^^^

    You can get only selected columns.

.. code:: python

    product_code = "co_10_jhucs_03"

    client = AltaDataAPI(YOUR_API_KEY)
    data = client.get_data(product_code)\
            .select(selected_column=["reported_date", "province_state", "mortality_rate"])\
            .load()



get the specified amount of data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    You can limit size of data.

    .. code:: python

        product_code = "co_10_jhucs_03"

        client = AltaDataAPI(YOUR_API_KEY)
        data = client.get_data(product_code, size=20).load()



Get Data with Multiple Conditions
-----------------------------------

    You can use multiple condition at same time.

    .. code:: python

        product_code = "co_10_jhucs_03"

        client = AltaDataAPI(YOUR_API_KEY)
        data = client.get_data(product_code, size=100)\
                    .condition_in(condition_column="province_state", condition_value=["Montana", "Utah"])\
                    .sort(order_column="mortality_rate", order_method="desc")\
                    .select(selected_column=["reported_date", "province_state", "mortality_rate"])\
                    .load()
