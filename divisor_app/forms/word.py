# divisor_app/forms/word.py

from django import forms

class WordForm(forms.Form):
    word = forms.CharField(
        label='Digite uma palavra (no singular)', min_length=2, max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Ex.: divisor'}),
    )

    def clean_word(self) -> str:
        return self.cleaned_data['word'].strip().lower()
