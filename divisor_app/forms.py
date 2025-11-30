import asyncio
from django import forms
from django.conf import settings
from .core.analyzer import WordAnalyzer
from better_profanity import profanity


# Loads the prohibited words to check bad behavior
try:
    with open(settings.RESTRICTED_WORDS_FILE, 'r', encoding='utf-8') as f:
        ptbr_badwords = [line.strip() for line in f.readlines()]
        profanity.add_censor_words(ptbr_badwords)
except FileNotFoundError:
    print(f"Arquivo não encontrado em {settings.RESTRICTED_WORDS_FILE}.")


class WordForm(forms.Form):
    word = forms.CharField (
        label='Digite uma palavra (no singular)', min_length=2, max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Ex.: divisor'})
    )

    def clean_word(self) -> str:
        """Verifies different cases for the user-supplied word.

        Raises:
            forms.ValidationError: If a bad word is found, raises an angry message.
            forms.ValidationError: If a easter egg is found, raises a message.
            forms.ValidationError: If the word is not alphabetical, raises a message.
            forms.ValidationError: If the word not exists in the dictionary, raises a message.

        Returns:
            str: If the user-supplied word is ok, returns it.
        """
        a = WordAnalyzer(self.cleaned_data['word'])

        if profanity.contains_profanity(a.word):
            raise forms.ValidationError("Tome cuidado com o que sai da sua boca (*`_´*)")

        if a.word in settings.EASTER_EGGS.keys():
            raise forms.ValidationError(settings.EASTER_EGGS[a.word])

        if not a.word.isalpha() and '-' not in a.word:
            raise forms.ValidationError("Por favor, digite apenas letras!")

        try:
            if not asyncio.run(a.word_exists()):
                raise forms.ValidationError(f"A palavra \"{a.word.upper()}\" não foi encontrada. " \
                                            +"Verifique se ela foi digitada corretamente ou " \
                                            +"se existe no dicionário brasileiro.")
        except Exception as e:
            print(f"Erro assíncrono ao verificar a existência da palavra: {e}")
            raise forms.ValidationError("Não foi possível verificar a palavra no momento. Tente novamente mais tarde.")

        return a.word


# class FeedbackForm(forms.Form):
#     feedback = forms.CharField (
#         label='Críticas, problemas na busca ou erros na divisão? Use o campo abaixo para falar conosco! ' \
#              +'Pedimos que forneça o máximo de detalhes para que possamos resolver o mais breve possível. ' \
#              +'Esteja ciente de que a análise não é perfeita e que pode apresentar falhas.',
#         max_length=100000, widget=forms.Textarea(attrs={'class': 'form-control mt-2', 'rows': 4})
#     )
