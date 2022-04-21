# from .client import EDIClient
from urllib.parse import parse_qs
from kenmall_enterprise_portal.config.settings import EDI_BASE_URL

edi_base_url = EDI_BASE_URL
EDI_V1_BASE_URL = edi_base_url + 'v1/'

edi_v1_enterprise_orders_base_url = EDI_V1_BASE_URL + 'enterprise_orders/'
edi_v1_debit_side_base_url = EDI_V1_BASE_URL + 'debit_side/'

# client = EDIClient()


class ListMixin(object):
    """List APIs"""

    def _parse_query_params(self, url, field):
        qs = url[url.index('?')+1:]
        query_params = parse_qs(qs)
        return query_params[field][0]

    def list_url(self):
        return self.base_url

    def list(self, filters=None):
        import pdb
        pdb.set_trace()
        url = EDI_V1_BASE_URL + self.list_url()
        pdb.set_trace()
        return self.connection.call(url, method='GET', params=filters)

    def iterate_cursor(
            self, filters=None, cursor_field='cursor', next_field='next',
            results_field='results'):
        params = {}

        if filters:
            params.update(filters)

        while True:
            result = self.list(params)

            for item in result[results_field]:
                yield item

            if not result[next_field]:
                break

            next_url = result[next_field]
            cursor = self._parse_query_params(next_url, cursor_field)
            params[cursor_field] = cursor

    def iterate(
            self, filters=None, page_start=None, page_end=None,
            page_field='page', results_field='results', next_field='next',
            page_size=None, page_size_field='page_size'):
        params = {}

        if filters:
            params.update(filters)

        if page_start:
            params[page_field] = page_start

        if page_size:
            params[page_size_field] = page_size

        while True:
            result = self.list(params)

            for item in result[results_field]:
                yield item

            if not result[next_field]:
                break

            next_url = result[next_field]
            page = int(self._parse_query_params(next_url, page_field))

            if page_end and page >= page_end:
                break

            params[page_field] = page


class CRUDMixin(ListMixin):
    """Simplify CRUD API wrappers.

    This mixin adds typical CRUD API operations/calls to simplify
    the making and maintenance of API wrappers.

    It requires that the class this is mixin into have the following
    class/instance attributes:

    - base_url: this is the base url of the API upon which the CRUD
      calls will be made.
    - connection: this is an object that actually performs the
      http requests (and any addon functionality). That is
      client.ApiConnection
    """

    # def detail_url(self, id):
    #     return urljoin(self.base_url, "{}/".format(id))

    def create(self, payload, files=None):
        url = self.list_url()
        return self.connection.call(
            url, method='POST', payload=payload, files=files)

    # @catch_404
    def get(self, id, params=None):
        """
        `params` kwargs is used to filter a single object and not a list.
        Filters such as `?filter_field=some_value` have no effect whatsoever.
        On the other hand, filters such as `?fields=field1,field2` will limit
        the fields returned in the results.
        """
        url = self.detail_url(id)
        return self.connection.call(url, method='GET', params=params)


class EDIEnterpriseUnits(CRUDMixin):

    def __init__(self, connection, base_url='units/'):
        self.connection = connection
        self.base_url = base_url


class EDIPurchasesOrder(CRUDMixin):
    """PurchasesOrder EDI CRUD operations access points."""

    def __init__(self, connection, base_url=''):
        self.connection = connection
        self.base_url = base_url


class EDIPurchasesOrderItem(CRUDMixin):
    """PurchasesOrderItem EDI CRUD operations access points."""

    def __init__(self, connection, base_url=''):
        self.connection = connection
        self.base_url = base_url


# class EDIPurchasesOrderAddresses:
#     """PurchasesOrderAddresses EDI CRUD operations access points."""

#     def __init__(self) -> None:
#         self.view_url = 'purshase_order_addresses/'
#         self.url = edi_v1_enterprise_orders_base_url + self.view_url

#     def get_purchases_orders_addresses(self):
#         schema = client.get(self.url)
#         return schema

#     def post_purchases_orders_addresses(self, payload):
#         client.post(self.url, payload)
#         pass


# # edienterpriseunits = EDIEnterpriseUnits()
# # edipurchasesorder = EDIPurchasesOrder()
# edipurchasesorderaddresses = EDIPurchasesOrderAddresses()


# class EDICalls:
#     def __init__(self) -> None:
#         pass

#     def get_edienterpriseunits(self=None):
#         return edienterpriseunits.get_units()

#     def post_edienterpriseunits(payload, self=None):
#         return edienterpriseunits.post_units(payload)

#     def get_edipurchasesorders(self=None):
#         return edipurchasesorder.get_purshase_orders()

#     def post_edipurchasesorders(payload, self=None):
#         return edipurchasesorder.post_purshase_orders(payload)

#     def get_edipurchasesorderaddresses(self=None):
#         return edipurchasesorderaddresses.get_purchases_orders_addresses()
    
#     def post_edipurchasesorderaddresses(payload, self=None):
#         return edipurchasesorderaddresses.post_purchases_orders_addresses(payload)
