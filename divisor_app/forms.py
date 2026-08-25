from better_profanity import profanity
from django import forms
from django.conf import settings

from .core.analyzer import DictionaryUnavailableError, WordAnalyzer

# Carrega a lista de palavras proibidas
try:
    with open(settings.RESTRICTED_WORDS_FILE, "r", encoding="utf-8") as f:
        ptbr_badwords = [line.strip() for line in f]
        profanity.add_censor_words(ptbr_badwords)
except FileNotFoundError:
    print(f"Arquivo não encontrado em {settings.RESTRICTED_WORDS_FILE}.")


class WordForm(forms.Form):
    word = forms.CharField(
        label="Digite uma palavra",
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
            forms.ValidationError: If the word is not found, raises an error message.
            forms.ValidationError: If the dictionary cannot be consulted, raises a failure message.

        Returns:
            str: If the user-supplied word is ok, returns it.
        """
        a = WordAnalyzer(self.cleaned_data["word"])

        if profanity.contains_profanity(a.word):
            raise forms.ValidationError("Palavra imprópria detectada!")

        if a.word in settings.EASTER_EGGS:
            raise forms.ValidationError(settings.EASTER_EGGS[a.word])

        if not a.word.isalpha() and "-" not in a.word:
            raise forms.ValidationError("Por favor, digite apenas letras!")

        try:
            if not a.word_exists():
                raise forms.ValidationError(
                    f'A palavra "{a.word.upper()}" não foi encontrada no dicionário português.'
                )
        except DictionaryUnavailableError:
            raise forms.ValidationError(
                "Não foi possível consultar o dicionário no momento. Tente novamente mais tarde."
            )

        return a.word
