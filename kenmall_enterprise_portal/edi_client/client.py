import uuid
import requests
from requests.exceptions import HTTPError, ConnectionError
from django.core.exceptions import ValidationError

val_err_msg = 'Server Connection Error. Contact admin'

class ApiConnection(object):

    """Handles authenticating and accessing a resource server.

    Parameters:
        host (str): edgeserver location in the format ``host[:port]``
        oauth_id (str): OAuth client ID
        oauth_secret (str): OAuth client secret
        user_email (str): User's email
        user_password (str): User's password
        scheme (str): ``http`` or ``https`` defaults to ``http``
        token_url (str): Endpoint to get tokens from the authserver
        scopes (list(str)): an array of strings describing the scopes.
        auth_retries (int or None): number of times to retry/reauthenticate
            a request if authentication failed. Use -1 for infinite retries.
        auth_retry_delay (float): (seconds) how long to wait before
            retrying auth failures. Use 0.0 to mean no delay.
        timeout_retries (int or None): number of times to retry
            a request if it timed out. Use -1 for infinite retries.
        timeout_retry_delay (float): (seconds) how long to wait before
            retrying timeout failures. Use 0.0 to mean no delay.
        connect_retries (int or None): number of times to retry a request
            if there's a connection error. Use -1 for infinite retries.
        connect_retry_delay (float): (seconds) how long to wait before
            retrying a request that failed on a connection error.
            Use 0.0 to mean no delay.
    """

    # RequestFailure = exceptions.RequestFailure
    # AuthFailure = exceptions.AuthFailure

    def __init__(self, host=None, oauth_id=None, oauth_secret=None, user_email=None,
                 user_password=None, scheme='https', token_url=None, scopes=None,
                 auth_retries=3, auth_retry_delay=1, timeout_retries=3,
                 timeout_retry_delay=1, connect_retries=3,
                 connect_retry_delay=1):
        """Authenticate the connection with the edgeserver."""

        assert scheme in ['http', 'https']
        self.host = host
        self.oauth_id = oauth_id
        self.oauth_secret = oauth_secret
        self.user_email = user_email
        self.user_password = user_password
        self.scheme = '{}://'.format(scheme)
        self.base_url = ApiConnection.urljoin(self.scheme, self.host)
        self.token_url = token_url
        self.auth_retries = auth_retries
        self.auth_retry_delay = auth_retry_delay
        self.timeout_retries = timeout_retries
        self.timeout_retry_delay = timeout_retry_delay
        self.connect_retries = connect_retries
        self.connect_retry_delay = connect_retry_delay

        self.base_headers = {
            'Accept': 'application/json, */*'
        }

        if self.token_url is not None:
            self.authenticate(self.token_url, scopes=scopes)

    def call(
        self, url, method='GET', params=None, payload=None, files=None,
        extra_headers=None, disable_json_parsing=False, is_stub=True):
        headers = []
        url = self.urljoin(self.base_url, url)

        return requests.request(method=method, url=url, params=params, data=payload, files=files, headers=headers)

    def urljoin(*urlparts):
        """
         url = urljoin('http://', 'google.com', 'mail')
            print url
            # prints 'http://google.com/mail'
        """
        # LOGGER.debug('Urljoin: urlparts={}'.format(urlparts))
        url = ''

        for part in urlparts:
            if part in ('', None):
                pass
            elif part == '/':
                if not url.endswith('/'):
                    url = "{}/".format(url)
            else:
                prt = str(part).strip().lstrip('/')
                if not url.endswith('/'):
                    try:
                        f = '/' if url != '' or part[0] == '/' else ''
                    except TypeError:
                        continue

                    prt = "{}{}".format(f, prt)
                url = "{}{}".format(url, prt)

        return url


class EDIClientt:
    """Make HTTP call.

        Uses the HTTP client to make a HTTP request to the provided
        url with the provided data. also handles filling in of the
        HTTP headers

        Parameters:
            url (str): the uri fragment to make the call to
            method (str): HTTP method to call
            params (dict): a dict to be sent as query parameters
            payload (dict): dict with the data to send with the call
                This will be serialized to json before being sent over.
            files (dict): dict with file data to send with the call
                e.g. {'model_file_field': open('path/file.pdf', 'rb')}
            extra_headers (dict): dict with any additional HTTP headers
                These will update the base headers.
            json_parsing (bool): parse the response as json or not.
                If False, reponse will be returned as JSON object.
                If True, response will be returned as a different Content-Type.

        """

    def __init__(self) -> None:
        self.err_status_codes = [400, 404]

    def get(self, url):
            # method='GET'
            # params = None
            # files=None
            # headers = {
            #     'Accept': 'application/json, */*'
            # }
            # response = requests.request(method=method, url=url, params=params, data=payload, files=files, headers=headers)
        try:
            response = requests.get(url)
            response.raise_for_status()

            return response.json()

        except ConnectionError as conn_err:
            conn_err_details = f"CONNECTION ERROR DETAILS: {conn_err}'"
            msg = 'Could not connect to the EDI Server. {}'.format(conn_err_details)
            # log this msg

        except HTTPError as http_err:
            err = f'HTTP POST error occurred: {http_err},'
            details  = response.text
            msg = f'{err} POST ERROR DETAILS: {details}'
            # log this msg
            raise HTTPError({'http_error': err})

    def post(self, url, payload):
        payload['created_by'] = uuid.uuid4()
        payload['updated_by'] = uuid.uuid4()
        import pdb
        pdb.set_trace()

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()

            return response.json()

        except HTTPError as http_err:
            err = f'HTTP POST error occurred: {http_err},'
            details  = response.text
            msg = f'{err} POST ERROR DETAILS: {details}'
            import pdb
            pdb.set_trace()
            # log this msg
            # raise ValidationError({'server error': val_err_msg})

        except ConnectionError as conn_err:
            conn_err_details = f"CONNECTION ERROR DETAILS: {conn_err}'"
            err = 'Could not connect to the EDI Server'
            msg = f'{err}. {conn_err_details}'
            raise ConnectionError({'edi_connection': err})
            import pdb
            pdb.set_trace()
            # log the msg
            # raise ValidationError({'server error': val_err_msg})

    def put(self, url, payload):
        url += 'put'
        response = requests.put(url, data=payload)

    def delete(self, url):
        url += 'delete'
        response = requests.delete(url)
        return response.json()

    def patch(self, url, payload):
        url += 'patch'
        response = requests.patch(url, data=payload)
        return response.json()

    def head(self, url):
        url += 'get'
        response = requests.head(url)
        return response.json()

    def options(self, url):
        url += 'get'
        response = requests.options(url)
        return response.json()

    def create_or_update_with(self, url,):
        self.connection.call()
        import pdb
        pdb.set_trace()

from . import connectors

DEFAULT_URL_MAP = {
    'units': (
        connectors.EDIEnterpriseUnits,
        '/debit_side/units/',),
    'purchases_orders': (
        connectors.EDIPurchasesOrder,
        '/enterprise_orders/purshases_orders/',),
    'purshases_order_items': (
        connectors.EDIPurchasesOrderItem,
        '/enterprise_orders/purshases_order_items/',),
}


class EDIClient(object):

    def __init__(self, config, url_map=None):
        base_url = config.pop('api_url', None)
        self.url_map = {}

        self.conn = ApiConnection(**config)
        if base_url:
            self.conn.base_url = self.conn.urljoin(
                self.conn.base_url, base_url)

        self.setup(url_map)

    def setup(self, url_map=None):
        if url_map is None:
            url_map = DEFAULT_URL_MAP

        self.url_map.update(url_map)
        for key in self.url_map:
            api_class = self.url_map[key][0]
            args = self.url_map[key][1:]
            api = api_class(self.conn, *args)
            setattr(self, key, api)
