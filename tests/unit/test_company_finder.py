from unittest import TestCase, mock
from app import company_finder
from requests.exceptions import HTTPError, RequestException, Timeout


class TestCompanyFinder(TestCase):

    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):

        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        mock_resp.status_code = status
        mock_resp.content = content
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    @mock.patch('app.company_finder.requests.get')
    def test_api_get_requester(self, mock_get_response):
        mock_response = self._mock_response(json_data=[{'title': 'test1', 'address': {'postcode': 'test1_pcode'}}])
        mock_get_response.return_value = mock_response

        result = company_finder._api_get_requester('test.com', 'api_test_key', 'test_payload')
        self.assertEqual(result, [{'title': 'test1', 'address': {'postcode': 'test1_pcode'}}])

    @mock.patch('app.company_finder.requests.get')
    def test_api_failed_get_requester(self, mock_get_response):
        mock_response = self._mock_response(status=501, raise_for_status=HTTPError("URL not found!"))
        mock_get_response.return_value = mock_response

        self.assertRaises(SystemExit, company_finder._api_get_requester, 'wrong_url', 'test_key', 'payload')

    @mock.patch('app.company_finder.requests.get')
    def test_api_failed_get_requester(self, mock_get_response):
        mock_response = self._mock_response(status=501, raise_for_status=HTTPError("URL not found!"))
        mock_get_response.return_value = mock_response

        self.assertRaises(SystemExit, company_finder._api_get_requester, 'wrong_url', 'test_key', 'payload')