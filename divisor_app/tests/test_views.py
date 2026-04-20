# divisor_app/tests/test_views.py

from django.urls import reverse
from django.test import TestCase

from unittest.mock import patch
from ..services.exceptions import CoreAPIError


class MainViewTests(TestCase):

    @patch('divisor_app.views.main.CoreAPIClient.analyze_word')
    def test_main_view_success(self, mock_analyze):
        mock_analyze.return_value = {
            'word': 'divisor',
            'divided_word': 'di-vi-sor',
            'reversed_syllables': 'sor-vi-di',
            'letters': None,
            'phonemes': None,
            'syllables': None,
            'stress': None,
            'vow_clusters': None,
            'con_clusters': None,
        }

        response = self.client.post(
            reverse('main-view'),
            data={
                'word': 'divisor',
                'submit_word': '1'
            }
        )

        self.assertEqual(response.status_code, 302)

    @patch('divisor_app.views.main.CoreAPIClient.analyze_word')
    def test_main_view_handles_api_404(self, mock_analyze):
        mock_analyze.side_effect = CoreAPIError(404, 'A palavra "DIVISOR" não consta no dicionário.')

        response = self.client.post(
            reverse('main-view'),
            data={
                'word': 'divisor',
                'submit_word': '1'
            },
            follow=True,
        )

        messages = list(response.context['messages'])
        self.assertTrue(any('não consta no dicionário' in str(m) for m in messages))

    @patch('divisor_app.views.main.CoreAPIClient.analyze_word')
    def test_main_view_handles_api_418(self, mock_analyze):
        mock_analyze.side_effect = CoreAPIError(418, 'Easter egg')

        response = self.client.post(
            reverse('main-view'),
            data={
                'word': 'divisor',
                'submit_word': '1'
            }, 
            follow=True,
        )

        messages = list(response.context['messages'])
        self.assertTrue(any('Easter egg' in str(m) for m in messages))
