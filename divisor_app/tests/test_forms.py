# divisor_app/tests/test_forms.py

from django.test import TestCase
from ..forms.word import WordForm


class WordFormTests(TestCase):

    def test_valid_word(self):
        form = WordForm(data={'word': 'Divisor'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['word'], 'divisor')

    def test_empty_word(self):
        form = WordForm(data={'word': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('word', form.errors)

    def test_strip_and_lower(self):
        form = WordForm(data={'word': '  SíLaBaS  '})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['word'], 'sílabas')
