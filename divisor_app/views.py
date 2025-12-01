from .forms import WordForm
from django.conf import settings
from .core.analyzer import WordAnalyzer
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
# from .forms import FeedbackForm
# from django.core.mail import send_mail


async def get_word_analysis_data(word: str) -> dict:
    """Async function to perform word analysis and return a dict with the results.

    Args:
        word (str): Contains the user-supplied word.

    Returns:
        dict: Contains the results of the word analysis.
    """
    a = WordAnalyzer(word)
    syllables = await a.get_syllables()

    return {
        'word': a.word,
        'syl_word': syllables,
        'tonicity': a.word_stress(),
        'num_letters': a.count_letters(),
        'num_phonemes': a.count_phonemes(),
        'vow_clusters': a.vowel_clusters(),
        'reversed': a.syllables_backwards(),
        'num_syllables': a.count_syllables(),
        'con_clusters': a.consonant_clusters(),
    }

def main_view(request):
    word_form = WordForm()
    # feedback_form = FeedbackForm()

    result = request.session.pop('result', None)
    error_messages = request.session.pop('error_messages', None)
    # feedback_success = request.session.pop('feedback_success', None)

    context = {
        'result': result,
        'word_form': word_form,
        'error_messages': error_messages,
        'feedback_email': settings.FEEDBACK_EMAIL,
        # 'feedback_form': feedback_form,
        # 'feedback_success': feedback_success,
    }

    if request.method == 'POST':
        if 'submit_word' in request.POST:
            word_form = WordForm(request.POST)
            if word_form.is_valid():
                try:
                    import asyncio; analysis_result = asyncio.run(get_word_analysis_data(word_form.cleaned_data['word']))
                    request.session['result'] = analysis_result
                except Exception as e:
                    word_form.add_error('word', ValidationError("Ocorreu um erro ao analisar a palavra. Tente novamente."))
                    request.session['error_messages'] = word_form.errors.get('word')
            else:
                request.session['error_messages'] = word_form.errors.get('word')
            return redirect('main-view')

        # elif 'submit_feedback' in request.POST:
        #     feedback_form = FeedbackForm(request.POST)
        #     if feedback_form.is_valid():
        #         feedback_text = feedback_form.cleaned_data['feedback']
        #         send_mail(
        #             subject='Feedback - Divisor de Sílabas',
        #             message=feedback_text,
        #             from_email=settings.EMAIL_HOST_USER,
        #             recipient_list=['jgabrielj.games77@gmail.com'],
        #             fail_silently=False,
        #         ); request.session['feedback_success'] = "Obrigado pelo seu feedback!"
        #     return redirect('main-view')

    return render(request, 'divisor_app/index.html', context)
