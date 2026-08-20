from better_profanity import profanity
from django import forms
from django.conf import settings

from .core.analyzer import WordAnalyzer

# Carrega a lista de palavras proibidas
try:
    with open(settings.RESTRICTED_WORDS_FILE, "r", encoding="utf-8") as f:
        ptbr_badwords = [line.strip() for line in f]
        profanity.add_censor_words(ptbr_badwords)
except FileNotFoundError:
    print(f"Arquivo não encontrado em {settings.RESTRICTED_WORDS_FILE}.")


class WordForm(forms.Form):
    word = forms.CharField(
        label="Digite uma palavra (no singular)",
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control mt-2", "placeholder": "Ex.: divisor"}
        ),
    )

    def clean_word(self) -> str:
        """Verifies different cases for the user-supplied word.

        Raises:
            forms.ValidationError: If a bad word is found, raises a warning message.
            forms.ValidationError: If a easter egg is found, raises a funny message.
            forms.ValidationError: If the word is not alphabetical, raises an alert message.
        Returns:
            str: If the user-supplied word is ok, returns it.
        """
        a = WordAnalyzer(self.cleaned_data["word"])

        if profanity.contains_profanity(a.word):
            raise forms.ValidationError("Palavra ruim detectada!")

        if a.word in settings.EASTER_EGGS:
            raise forms.ValidationError(settings.EASTER_EGGS[a.word])

        if not a.word.isalpha() and "-" not in a.word:
            raise forms.ValidationError("Por favor, digite apenas letras!")

        return a.word
