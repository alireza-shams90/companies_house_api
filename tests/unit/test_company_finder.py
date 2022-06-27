from unittest import TestCase, mock
from app import company_finder
from requests.exceptions import HTTPError, Timeout
import json
from os import path


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
    def test_api_failed_get_requester_http(self, mock_get_response):
        mock_response = self._mock_response(status=501, raise_for_status=HTTPError("URL not found!"))
        mock_get_response.return_value = mock_response

        self.assertRaises(SystemExit, company_finder._api_get_requester, 'wrong_url', 'test_key', 'payload')

    @mock.patch('app.company_finder.requests.get')
    def test_api_failed_get_requester_timeout(self, mock_get_response):
        mock_response = self._mock_response(status=504, raise_for_status=Timeout("Timeout error! Will sleep for a minute"
                                                                                 "and then fails with another Timeout error"
                                                                                 "and SystemExit"))
        mock_get_response.return_value = mock_response

        self.assertRaises(SystemExit, company_finder._api_get_requester, 'wrong_url', 'test_key', 'payload')

    @mock.patch('app.company_finder._api_get_requester')
    def test_search_companies(self, mock_api_get_requester):
        pth = path.join(path.dirname(__file__), "test_response.json")
        f = open(path.join(path.dirname(__file__), "test_response.json"))
        mock_api_get_requester.return_value = json.loads(f.read())
        f.close()
        results = company_finder.search_companies('test', 10, 0)


        expected_output = [('07500445', 'SONOVATE LIMITED', 'ltd', '2011-01-20', '2022-05-15', 'Floor Golate House',
                            '4th', 'Cardiff', 'Wales', 'CF10 1DX', 'active', 'incorporated-on', '4')]
        self.assertEqual(results, expected_output)
