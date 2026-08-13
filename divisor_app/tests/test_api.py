#! divisor_app/tests/test_analyzer.py

from unittest.mock import Mock, patch

from django.test import TestCase

from ..services.core_api import CoreAPIClient
from ..services.exceptions import CoreAPIError


class CoreAPIClientTests(TestCase):
    @patch("divisor_app.services.core_api.requests.post")
    def test_analyze_word_success(self, mock_post):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "word": "divisor",
            "divided_word": "di-vi-sor",
        }
        mock_post.return_value = mock_response

        client = CoreAPIClient()
        data = client.analyze_word("divisor")

        self.assertEqual(data["word"], "divisor")

    @patch("divisor_app.services.core_api.requests.post")
    def test_analyze_word_error_with_detail(self, mock_post):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.json.return_value = {
            "detail": 'A palavra "DIVISOR" não consta no dicionário.',
        }
        mock_post.return_value = mock_response

        client = CoreAPIClient()
        with self.assertRaises(CoreAPIError) as ctx:
            client.analyze_word("divisor")

        self.assertEqual(ctx.exception.status_code, 404)
        self.assertIn("não consta no dicionário", ctx.exception.message)

    @patch("divisor_app.services.core_api.requests.post")
    def test_analyze_word_error_without_json(self, mock_post):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.json.side_effect = ValueError()
        mock_post.return_value = mock_response

        client = CoreAPIClient()
        with self.assertRaises(CoreAPIError) as ctx:
            client.analyze_word("divisor")

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertEqual(ctx.exception.message, "Internal Server Error")
