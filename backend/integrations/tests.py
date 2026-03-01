import json
from django.test import TestCase, override_settings
from unittest.mock import patch, Mock
import requests
from .greenweb import GreenwebClient

class GreenwebClientTests(TestCase):
    def setUp(self):
        pass

    @override_settings(GREENWEB_TOKEN='')
    @patch('integrations.greenweb.requests.post')
    def test_send_sms_no_token(self, mock_post):
        # Ensure token is missing via settings override
        client = GreenwebClient()
        response = client.send_sms('01711111111', 'Test message')

        self.assertIsNone(response)
        mock_post.assert_not_called()

    @override_settings(GREENWEB_TOKEN='test_token')
    @patch('integrations.greenweb.requests.post')
    def test_send_sms_prepends_88_to_01_numbers(self, mock_post):
        # Mock a successful response
        mock_response = Mock()
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response

        client = GreenwebClient()
        client.send_sms('01711111111', 'Test message')

        # Check that post was called with correctly formatted number
        mock_post.assert_called_once()
        call_args, call_kwargs = mock_post.call_args

        payload = json.loads(call_kwargs['data'])

        self.assertEqual(payload['smsdata'][0]['to'], '+8801711111111')
        self.assertEqual(payload['smsdata'][0]['message'], 'Test message')
        self.assertEqual(payload['token'], 'test_token')

    @override_settings(GREENWEB_TOKEN='test_token')
    @patch('integrations.greenweb.requests.post')
    def test_send_sms_leaves_plus_88_numbers_alone(self, mock_post):
        # Mock a successful response
        mock_response = Mock()
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response

        client = GreenwebClient()
        client.send_sms('+8801711111111', 'Test message')

        mock_post.assert_called_once()
        call_args, call_kwargs = mock_post.call_args

        payload = json.loads(call_kwargs['data'])

        self.assertEqual(payload['smsdata'][0]['to'], '+8801711111111')

    @override_settings(GREENWEB_TOKEN='test_token')
    @patch('integrations.greenweb.requests.post')
    def test_send_sms_leaves_other_numbers_alone(self, mock_post):
        # Mock a successful response
        mock_response = Mock()
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response

        client = GreenwebClient()
        # Not starting with 01 or +88
        client.send_sms('123456789', 'Test message')

        mock_post.assert_called_once()
        call_args, call_kwargs = mock_post.call_args

        payload = json.loads(call_kwargs['data'])

        self.assertEqual(payload['smsdata'][0]['to'], '123456789')

    @override_settings(GREENWEB_TOKEN='test_token')
    @patch('integrations.greenweb.requests.post')
    def test_send_sms_handles_request_exception(self, mock_post):
        # Simulate a request failure
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        client = GreenwebClient()
        response = client.send_sms('+8801711111111', 'Test message')

        self.assertIsNone(response)
        mock_post.assert_called_once()
