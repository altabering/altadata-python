"""
Python library for the ALTADATA API.

This API was built with the developer in mind and should allow a developer
to build applications around the ALTADATA API without having to deal with
accessing and managing the requests and responses.
"""
import requests
import json
from pandas import DataFrame
from pandas import to_datetime
from typing import Union, List


class AltaDataAPI:
    """
    This is the main class of the API module. It contains all of the data API logic.
    """

    def __init__(self, api_key: str):
        """
        AltaDataAPI constructor. Sets the response format on all of the URLs and the api key required to access the API.

        :param api_key: ALTADATA API key
        """
        self.api_key = api_key
        self.data_api_url = "https://www.altadata.io/data/api/"
        self.subscription_api_url = "https://www.altadata.io/subscription/api/"
        self.export_format = "json"

    def _fix_subscription_response(self, response_json):
        """A private method to convert subscription api response to unnested version"""
        data = []

        for product in response_json:
            product_item = product
            product_item["createdAt"] = (
                product_item["createdAt"].split("T")[0]
                + " "
                + product_item["createdAt"].split("T")[1][:5]
            )
            product_item["validUntil"] = (
                product_item["validUntil"].split("T")[0]
                + " "
                + product_item["validUntil"].split("T")[1][:5]
            )
            product_item["title"] = product_item["offer"]["title"]
            product_item["code"] = product_item["offer"]["code"]
            product_item["price"] = product_item["plan"]["price"]
            product_item["plan_name"] = product_item["plan"]["title"]
            product_item["period"] = product_item["plan"]["period"]

            del product_item["id"]
            del product_item["offer"]
            del product_item["plan"]

            data.append(product_item)

        return data

    def _list_subscription(
        self, return_as_dataframe: bool = True
    ) -> Union[List[dict], DataFrame]:

        request_url = (
            self.subscription_api_url + "subscriptions?api_key=" + self.api_key
        )
        response = requests.get(request_url, headers={"Authorization": self.api_key})

        response_json = json.loads(response.content)
        data = self._fix_subscription_response(response_json)

        if return_as_dataframe:
            data = DataFrame(data)
            data["createdAt"] = to_datetime(data["createdAt"])
            data["validUntil"] = to_datetime(data["validUntil"])

        return data

    def _get_header(self, product_code: str):
        request_url = (
            self.data_api_url
            + product_code
            + "/?format="
            + self.export_format
            + "&page=1"
        )
        response = requests.get(request_url, headers={"Authorization": self.api_key})
        header = list(json.loads(response.content)[0].keys())

        return header

    def _fetch_data(self) -> Union[List[dict], DataFrame]:
        data = []
        page = 1
        total_size = 0

        while True:
            request_url = self.__request_url_base + "&page=" + str(page)
            response = requests.get(
                request_url, headers={"Authorization": self.api_key}
            )

            if not response.status_code == 200:
                raise ConnectionError(str(response.content))

            response_json = json.loads(response.content)

            if len(response_json) < 1:
                break

            data += response_json

            if self.size is not None:
                total_size += len(response_json)

                if total_size > self.size:
                    break

            page += 1

        if self.size is not None:
            data = data[: self.size]

        if self.return_as_dataframe:
            data = DataFrame(data)

        return data

    def list_subscription(
        self, return_as_dataframe: bool = True
    ) -> Union[List[dict], DataFrame]:
        """
        List customer's subscriptions

        :param return_as_dataframe: Return as dataframe flag
        :returns: if return_as_dataframe parameter is False returns **list of dict** otherwise returns **pandas dataframe**.
        """
        if type(return_as_dataframe) is not bool:
            raise TypeError("return_as_dataframe parameter must be boolean")

        data = self._list_subscription(return_as_dataframe)

        return data

    def get_header(self, product_code: str):
        """
        Get data header

        :param product_code: Data product code
        :rtype: list
        """
        if type(product_code) is not str:
            raise TypeError("product_code parameter must be string")

        header = self._get_header(product_code)

        return header

    def get_data(self, product_code: str, size: int = None, return_as_dataframe=True):
        """
        Initialize retrieve data process

        :param product_code: Data product code
        :param size: Data size
        :param return_as_dataframe: Return as dataframe flag
        """
        if type(product_code) is not str:
            raise TypeError("product_code parameter must be string")

        if size is not None:
            if type(size) is not int:
                raise TypeError("size parameter must be integer")
            elif size <= 0:
                raise ValueError("size parameter must be greater than 0")

        if type(return_as_dataframe) is not bool:
            raise TypeError("return_as_dataframe parameter must be boolean")

        self.size = size
        self.return_as_dataframe = return_as_dataframe
        self.__request_url_base = (
            self.data_api_url + product_code + "/?format=" + self.export_format
        )

        return self

    def select(self, selected_column: list):
        """
        Select specific columns

        :param selected_column: List of columns to choose
        """
        if type(selected_column) is not list:
            raise TypeError("selected_column parameter must be list")
        elif len(selected_column) < 1:
            raise ValueError(
                "selected_column parameter must contain at least one value"
            )

        selected_column_text = ",".join([item for item in selected_column])
        self.__request_url_base += "&columns=" + selected_column_text

        return self

    def sort(self, order_column: str = None, order_method: str = "asc"):
        """
        Sort data by given column and method

        :param order_column: Column to which the order is applied
        :param order_method: Sorting method. Posibble values: asc or desc
        """
        if type(order_column) is not str:
            raise TypeError("order_column parameter must be string")
        elif type(order_method) is not str:
            raise TypeError("order_method parameter must be string")
        elif order_method not in ["asc", "desc"]:
            raise ValueError("order_method parameter must be 'asc' or 'desc'")

        self.__request_url_base += "&order_by=" + order_column + "_" + order_method

        return self

    def equal(self, condition_column: str = None, condition_value=None):
        """
        'Equal' condition by given column and value

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")

        self.__request_url_base += (
            "&" + condition_column + "_eq=" + str(condition_value)
        )

        return self

    def not_equal(self, condition_column: str = None, condition_value=None):
        """
        'Not equal' condition by given column and value

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")

        self.__request_url_base += (
            "&" + condition_column + "_neq=" + str(condition_value)
        )

        return self

    def greater_than(self, condition_column: str = None, condition_value=None):
        """
        'Greater than' condition by given column and value

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")

        self.__request_url_base += (
            "&" + condition_column + "_gt=" + str(condition_value)
        )

        return self

    def greater_than_equal(self, condition_column: str = None, condition_value=None):
        """
        'Greater than equal' condition by given column and value

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")

        self.__request_url_base += (
            "&" + condition_column + "_gte=" + str(condition_value)
        )

        return self

    def less_than(self, condition_column: str = None, condition_value=None):
        """
        'Less than' condition by given column and value

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")

        self.__request_url_base += (
            "&" + condition_column + "_lt=" + str(condition_value)
        )

        return self

    def less_than_equal(self, condition_column: str = None, condition_value=None):
        """
        'Less than equal' condition by given column and value

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")

        self.__request_url_base += (
            "&" + condition_column + "_lte=" + str(condition_value)
        )

        return self

    def condition_in(self, condition_column: str = None, condition_value=None):
        """
        'In' condition by given column and value list

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")
        elif type(condition_value) is not list:
            raise TypeError("condition_value parameter must be list")

        condition_value_text = ",".join([item for item in condition_value])
        self.__request_url_base += (
            "&" + condition_column + "_in=" + condition_value_text
        )

        return self

    def condition_not_in(self, condition_column: str = None, condition_value=None):
        """
        'Not in' condition by given column and value list

        :param condition_column: column to which the condition will be applied
        :param condition_value: value to use with condition
        """
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")
        elif type(condition_value) is not list:
            raise TypeError("condition_value parameter must be list")

        condition_value_text = ",".join([item for item in condition_value])
        self.__request_url_base += (
            "&" + condition_column + "_notin=" + condition_value_text
        )

        return self

    def load(self) -> Union[List[dict], DataFrame]:
        """
        Fetch data with configurations given before

        :returns: if return_as_dataframe parameter is False returns list of dict otherwise returns pandas dataframe.
        """

        data = self._fetch_data()

        return data
