# divisor_app/views/feedback.py

from django.contrib import messages
from django.shortcuts import render, redirect
from ..services.exceptions import (
    SITE_MESSAGES,
    FeedbackSendError,
)

from asgiref.sync import async_to_sync
from ..forms.feedback import FeedbackForm
from ..services.email import send_feedback


def feedback_view(request):
    feedback_form = FeedbackForm(request.POST or None)

    if request.method == 'POST':
        if feedback_form.is_valid():
            try:
                async_to_sync(send_feedback)(
                    feedback_form.cleaned_data['feedback'],
                    feedback_form.cleaned_data['email'],
                )

                messages.success(request, SITE_MESSAGES['email_success'])
                return redirect('feedback-view')

            except FeedbackSendError:
                messages.error(request, SITE_MESSAGES['unable_to_send'])

            except Exception:
                messages.error(request, SITE_MESSAGES['internal_error'])

    return render(request, 'divisor_app/feedback.html', {
        'feedback_form': feedback_form,
    })
