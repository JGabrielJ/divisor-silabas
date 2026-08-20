import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .core.analyzer import WordAnalyzer
from .forms import WordForm

logger = logging.getLogger(__name__)


def get_word_analysis_data(word: str) -> dict:
    """Performs word analysis and returns a dict with the results.

    Args:
        word (str): Contains the user-supplied word.

    Returns:
        dict: Contains the results of the word analysis.
    """
    a = WordAnalyzer(word)
    syllables = a.get_syllables()

    return {
        "word": a.word,
        "syl_word": syllables,
        "num_letters": a.count_letters(),
        "num_phonemes": a.count_phonemes(),
        "num_syllables": a.count_syllables(),
        "tonicity": a.word_stress(),
        "vow_clusters": a.vowel_clusters(),
        "con_clusters": a.consonant_clusters(),
        "reversed": a.syllables_backwards(),
    }


def main_view(request):
    word_form = WordForm()

    result = request.session.pop("result", None)
    error_messages = request.session.pop("error_messages", None)

    context = {
        "result": result,
        "word_form": word_form,
        "error_messages": error_messages,
        "paypal_donation_url": settings.PAYPAL_DONATION_URL,
    }

    if request.method == "POST" and "submit_word" in request.POST:
        word_form = WordForm(request.POST)
        if word_form.is_valid():
            try:
                analysis_result = get_word_analysis_data(word_form.cleaned_data["word"])
                request.session["result"] = analysis_result
            except Exception:
                logger.exception("Erro ao analisar a palavra enviada.")
                word_form.add_error(
                    "word",
                    ValidationError(
                        "Ocorreu um erro ao analisar a palavra. Tente novamente."
                    ),
                )
                request.session["error_messages"] = word_form.errors.get("word")
        else:
            request.session["error_messages"] = word_form.errors.get("word")
        return redirect("main-view")

    return render(request, "divisor_app/index.html", context)
