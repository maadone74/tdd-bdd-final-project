######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Steps

Steps file for products.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given
from service.common import status  # HTTP Status Codes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions



@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    #
    # List all of the products and delete them one by one
    #
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == status.HTTP_200_OK or context.resp.status_code == status.HTTP_404_NOT_FOUND)
    if (context.resp.status_code == 200):
        for product in context.resp.json():
            context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
            assert(context.resp.status_code == status.HTTP_204_NO_CONTENT)

    #
    # load the database with new products
    #
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert(context.resp.status_code == status.HTTP_201_CREATED)


@when(u'I press the "{button}" button')
def step_impl(context,button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()


@then(u'I should see the message "{msg}"')
def step_impl(context,msg):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            msg
        )
    )
    assert(found)


@then(u'I should see "{text}" in the results')
def step_impl(context,text):
    found1 = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            text
        )
    )
    assert(found1)


@then(u'I should not see "{text}" in the results')
def step_impl(context,text):
    element = context.driver.find_element_by_id('search_results')
    assert(text not in element.text)
