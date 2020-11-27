"""
Python library for the ALTADATA API

This Python library allows a developer to build applications around the ALTADATA API
without having to deal with accessing and managing the requests and responses.
"""
import requests
import json

try:
    from pandas import DataFrame
    from pandas import to_datetime

    pandas_installed = True
except ImportError:
    pandas_installed = False


class AltaDataAPI:
    """
    This is the main class of the API module. It contains all of the data API logic.
    """

    def __init__(self, api_key: str, dataframe_functionality: bool = False):
        """
        AltaDataAPI constructor. Sets the response format on all of the URLs and the api key required to access the API.

        :param api_key: ALTADATA API key
        :param dataframe_functionality: If dataframe_functionality is True list_subscription and get_data functions returns pandas dataframe otherwise returns list of dict.
        """
        self.api_key = api_key
        self.data_api_url = "https://www.altadata.io/data/api/"
        self.subscription_api_url = "https://www.altadata.io/subscription/api/"
        self.dataframe_functionality = dataframe_functionality

        if type(api_key) is not str:
            raise TypeError("api_key parameter must be string")

        if type(dataframe_functionality) is not bool:
            raise TypeError("dataframe_functionality parameter must be boolean")

        if not pandas_installed and dataframe_functionality:
            raise RuntimeError(
                "dataframe_functionality requires pandas (v0.23 or above) to work"
            )

    def _fix_subscription_response(self, response_json):
        """A private method to convert subscription api response to unnested version"""
        data = []

        for product in response_json:
            product_item = product
            product_item["createdAt"] = (
                product_item["createdAt"].replace("T", " ").split("+")[0]
            )
            product_item["validUntil"] = (
                product_item["validUntil"].replace("T", " ").split("+")[0]
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

    def _list_subscription(self):

        request_url = (
            self.subscription_api_url + "subscriptions?api_key=" + self.api_key
        )
        response = requests.get(request_url, headers={"Authorization": self.api_key})

        response_json = json.loads(response.content)
        data = self._fix_subscription_response(response_json)

        if self.dataframe_functionality:
            data = DataFrame(data)
            data["createdAt"] = to_datetime(data["createdAt"])
            data["validUntil"] = to_datetime(data["validUntil"])

        return data

    def _get_header(self, product_code: str):
        request_url = self.data_api_url + product_code + "/?format=json&page=1"
        response = requests.get(request_url, headers={"Authorization": self.api_key})
        header = list(json.loads(response.content)[0].keys())

        return header

    def _check_parameters(self, condition_column, condition_value_list=None):
        """A private method for controlling types of parameters"""
        if type(condition_column) is not str:
            raise TypeError("condition_column parameter must be string")

        if condition_value_list is not None:
            if type(condition_value_list) is not list:
                raise TypeError("condition_value parameter must be list")

    def _fetch_data(self):
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

            if self.limit is not None:
                total_size += len(response_json)

                if total_size > self.limit:
                    break

            page += 1

        if self.limit is not None:
            data = data[: self.limit]

        if self.dataframe_functionality:
            data = DataFrame(data)

        return data

    def list_subscription(self):
        """
        List customer's subscriptions

        :returns: if dataframe_functionality parameter is False returns **list of dict** otherwise returns **pandas dataframe**.
        """

        data = self._list_subscription()

        return data

    def get_header(self, product_code: str):
        """
        Get data header as a list

        :param product_code: Data product code
        :rtype: list
        """
        if type(product_code) is not str:
            raise TypeError("product_code parameter must be string")

        header = self._get_header(product_code)

        return header

    def get_data(self, product_code: str, limit: int = None):
        """
        Initialize retrieve data process

        :param product_code: Data product code
        :param limit: Number of rows you want to retrieve
        """
        if type(product_code) is not str:
            raise TypeError("product_code parameter must be string")

        if limit is not None:
            if type(limit) is not int:
                raise TypeError("limit parameter must be integer")
            elif limit <= 0:
                raise ValueError("limit parameter must be greater than 0")

        self.limit = limit
        self.__request_url_base = self.data_api_url + product_code + "/?format=json"

        return self

    def select(self, selected_column: list):
        """
        Select specific columns in the retrieve data process

        :param selected_column: List of columns to select
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
        Sort data by given column and method in the retrieve data process

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
        'Equal' condition by given column and value in the retrieve data process

        :param condition_column: Column to which the condition will be applied
        :param condition_value: Value to use with condition
        """
        self._check_parameters(condition_column=condition_column)

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
        self._check_parameters(condition_column=condition_column)

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
        self._check_parameters(condition_column=condition_column)

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
        self._check_parameters(condition_column=condition_column)

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
        self._check_parameters(condition_column=condition_column)

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
        self._check_parameters(condition_column=condition_column)

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
        self._check_parameters(
            condition_column=condition_column, condition_value_list=condition_value
        )

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
        self._check_parameters(
            condition_column=condition_column, condition_value_list=condition_value
        )

        condition_value_text = ",".join([item for item in condition_value])
        self.__request_url_base += (
            "&" + condition_column + "_notin=" + condition_value_text
        )

        return self

    def load(self):
        """
        Fetch data with configurations given before

        :returns: if dataframe_functionality parameter is True returns pandas dataframe otherwise returns list of dict.
        """

        data = self._fetch_data()

        return data
