--------------------------
Get Header
--------------------------

You can get your data header with the code below.

Firstly import library with the code below.

.. code:: python

    from altadata.altadata import *


.. code:: python

    client = AltaDataAPI(YOUR_API_KEY)
    header = client.get_header(PRODUCT_CODE)


:func:`~altadata.AltaDataAPI.get_header` returns **list**.
