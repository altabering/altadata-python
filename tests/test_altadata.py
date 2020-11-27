# coding: utf-8
import sys
import os
import time
from random import randint

sys.path.append("../")
from altadata import altadata

PRODUCT_CODE = "co_10_jhucs_03"
API_KEY = os.environ["TEST_API_KEY"]
client = altadata.AltaDataAPI(api_key=API_KEY, dataframe_functionality=True)


def test_list_subscription():
    sleep_time = randint(1, 3)
    time.sleep(sleep_time)

    assert client.list_subscription()["code"].tolist() == [
        "CO_10_JHUCS_04",
        "CO_08_UNXXX_04",
        "CO_10_JHUCS_03",
        "CO_07_IDEAX_02",
    ]


def test_get_header():
    sleep_time = randint(1, 3)
    time.sleep(sleep_time)

    assert client.get_header(PRODUCT_CODE) == [
        "reported_date",
        "province_state",
        "population",
        "lat",
        "lng",
        "confirmed",
        "prev_confirmed_1d",
        "new_confirmed",
        "peak_confirmed_1d_flag",
        "active",
        "deaths",
        "prev_deaths_1d",
        "new_deaths",
        "most_deaths_1d_flag",
        "recovered",
        "hospitalization_rate",
        "incidence_rate",
        "mortality_rate",
        "people_hospitalized",
        "people_tested",
        "testing_rate",
    ]


def test_get_data_with_sort():
    sleep_time = randint(1, 3)
    time.sleep(sleep_time)

    data = (
        client.get_data(product_code=PRODUCT_CODE, limit=10)
        .equal(condition_column="province_state", condition_value="Alabama")
        .sort(order_column="reported_date", order_method="asc")
        .load()
    )

    assert data["reported_date"].values[0] == "2020-04-12"


def test_get_data_with_select():
    sleep_time = randint(1, 3)
    time.sleep(sleep_time)

    data = (
        client.get_data(product_code=PRODUCT_CODE, limit=10)
        .select(selected_column=["reported_date", "province_state", "mortality_rate"])
        .load()
    )

    assert data.columns.tolist() == [
        "reported_date",
        "province_state",
        "mortality_rate",
    ]


def test_get_data_with_in():
    sleep_time = randint(1, 3)
    time.sleep(sleep_time)

    data = (
        client.get_data(product_code=PRODUCT_CODE, limit=250)
        .condition_in(
            condition_column="province_state", condition_value=["Montana", "Utah"]
        )
        .load()
    )

    assert data["province_state"].unique().tolist() == ["Montana", "Utah"]


def test_get_data_with_not_in():
    sleep_time = randint(1, 3)
    time.sleep(sleep_time)

    check_list = ["Montana", "Utah", "Alabama"]

    data = (
        client.get_data(product_code=PRODUCT_CODE, limit=250)
        .condition_not_in(
            condition_column="province_state", condition_value=check_list,
        )
        .load()
    )

    province_state_list = data["province_state"].unique().tolist()

    assert not any(x in province_state_list for x in check_list)
