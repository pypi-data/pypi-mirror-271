import os
import json
import requests
import datetime

from dotenv import load_dotenv

from .order_statuses import OrderStatus, validate_order_status

class AmazonSDK:
    # exported functions do not check params but check the returned status code
    def __init__(self, dotenv_path: str = None):
        """
        Initializes the AmazonSDK object with the given dotenv file path.
        :param dotenv_path: path to the dotenv file.
        """
        self.MARKETPLACE_IDS = ["A1805IZSGTT6HS"]
        self.ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
        # print 1+1

        # =============================================================================
        # Calling the API credentials:
        # ----------------------------
        load_dotenv(dotenv_path=dotenv_path)
        self._amz_client_id = os.environ.get('LWA_APP_ID')
        self._amz_client_secret = os.environ.get('LWA_CLIENT_SECRET')
        self._amz_refresh_token = os.environ.get('SP_API_REFRESH_TOKEN')
        #
        # ==============================================================================

        # regular access_token grants no access for PII, e.g. buyer name, address lines, etc.
        self.access_token = self._get_access_token()
        # self.access_token = self._get_restricted_data_token()  # no need anymore: ask for permission for PII

        # Use session to store the access token
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AmazonSDK/1.0 (Language=Python)',
            'x-amz-access-token': self.access_token,
        })

    def _get_access_token(self) -> str:
        """
        Fetches an access token using var loaded from .env file.

        :return: access token.
        """
        path = "https://api.amazon.com/auth/o2/token"
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._amz_refresh_token,
            'client_id': self._amz_client_id,
            'client_secret': self._amz_client_secret,
        }
        response = requests.post(path, data=data)
        assert response.status_code == 200, response.text
        return response.json()['access_token']

    def _get_restricted_data_token(self) -> str:
        """
        Fetches a restricted data token.
        POST /tokens/2021-03-01/restrictedDataToken, Rate (requests per second) = 1, Burst = 10
        :return: restricted data token.
        """
        path = "/tokens/2021-03-01/restrictedDataToken"
        data = {
            "restrictedResources":
                [
                    {
                        "method": "GET",
                        "path": "/orders/v0/orders",
                        "dataElements": ["buyerInfo",
                                         "shippingAddress",
                                         "buyerTaxInformation"]  # all data elements
                        # "buyerTaxInformation" is only available in the Turkey marketplace for the orders that
                        # BuyerInvoicePreference is BUSINESS.
                    }
                ]
        }
        response = requests.post(self.ENDPOINT + path, json=data, headers={
            'User-Agent': 'AmazonSDK/1.0 (Language=Python)',
            'x-amz-access-token': self.access_token,
        })
        assert response.status_code == 200, response.text
        return response.json()['restrictedDataToken']

    def get_one_order(self, order_id: str) -> dict:
        """
        Fetches one order by order_id.
        GET /orders/v0/orders/{orderId}, Rate (requests per second) = 0.5, Burst = 30
        :param order_id: An Amazon-defined order identifier, in 3-7-7 format, e.g. 408-8415756-8354712 (this is valid)
        :return: a dict containing the order information
        """
        path = f"/orders/v0/orders/{order_id}"
        response = self.session.get(self.ENDPOINT + path)
        assert response.status_code == 200, response.text
        return response.json()['payload']

    # FIXME: MID. quota may be exceeded if too many pages, need backoff
    def _get_a_page_of_orders(self, statuses: list[OrderStatus] = None,
                              created_after: str = '1970-01-01',
                              created_before: str = None,
                              next_token: str = None) -> dict:
        """
        Fetches a page of orders, max 100 orders per page.
        GET /orders/v0/orders, Rate (requests per second) = 0.0167, Burst = 20
        :param next_token: Token to fetch the next page of orders.
        :return: response payload, i.e. a dict containing a list of orders and optionally a next token.
        """
        path = "/orders/v0/orders"
        params = {
            'MarketplaceIds': ','.join(self.MARKETPLACE_IDS),
            'CreatedAfter': created_after,
            # =============================================================================
            # # test pagination
            # 'MaxResultsPerPage': 5
            # =============================================================================
        }
        if statuses:
            #  OrderStatuses MUST be a comma-separated string containing the statuses, to be properly url-encoded
            params['OrderStatuses'] = ','.join([s.value for s in statuses])
        if created_before:
            params['CreatedBefore'] = created_before
        if next_token:
            params['NextToken'] = next_token
        response = self.session.get(self.ENDPOINT + path, params=params)
        assert response.status_code == 200, response.text
        return response.json()['payload']

    def get_all_orders(self, statuses: list[OrderStatus] = None,
                       created_on: str = None,
                       created_after: str = '1970-01-01',
                       created_before: str = None,
                       ) -> tuple[list[dict], int]:
        """
        Fetches all orders created after a certain date.

        # troubleshooting: 1. pagination, 2. rate limit, 3. restricted data token (RDT), etc.
        :param statuses: Enum OrderStatus, possible values:
        Pending, Unshipped, PartiallyShipped, Shipped, Canceled, Unfulfillable, InvoiceUnconfirmed, PendingAvailability.
        :param created_on: Fetch orders created on this date, must be in ISO 8601 format.
        if provided, created_after and created_before are ignored.
        :param created_after: Fetch orders created after this time, must be in ISO 8601 format.
        :param created_before: Fetch orders created before this time, must be in ISO 8601 format.
        created_before should be equal to or after the CreatedAfter date and at least 2 minutes before the current time.
        :return: (a list of all orders, number of pages)
        """
        if created_on:
            created_after = created_on + 'T00:00:00Z'
            created_before = (datetime.datetime.fromisoformat(created_on) + datetime.timedelta(days=1)).isoformat() + 'Z'

        # results has a max of 100 orders per page, so we need to paginate
        orders = []
        next_token = None
        n_requests = 0
        while True:
            n_requests += 1
            payload = self._get_a_page_of_orders(statuses, created_after, created_before, next_token)
            orders_in_this_page = payload['Orders']
            orders.extend(orders_in_this_page)
            next_token = payload.get('NextToken')
            if not next_token:
                break
        # FIXME: LOW. with MaxResultsPerPage = 5, n_requests would be 3 for 10 orders, the last order list being emtpy
        return orders, n_requests


if __name__ == '__main__':
    sdk = AmazonSDK()
    all_orders, n_req = sdk.get_all_orders()
    print(json.dumps(all_orders, indent=2))
    print('Number of all orders:', len(all_orders))
    print('Number of pages:', n_req)
    pass
