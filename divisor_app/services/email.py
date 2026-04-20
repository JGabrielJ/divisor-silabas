# divisor_app/services/email.py

from django.conf import settings
from .exceptions import FeedbackSendError

import requests
from asgiref.sync import sync_to_async


async def send_feedback(text: str, user_email: str) -> None:
    """Envia um feedback através de um formulário no Google Forms.

    Args:
        text (str): O conteúdo da mensagem de feedback.
        user_email (str): O endereço de e-mail do usuário.
    
    Raises:
        FeedbackSendError: Se o form retornar um código diferente de 200 OK ou 302 Found.
        FeedbackSendError: Se ocorrer um erro inesperado.
    """
    data = {
        settings.GOOGLE_FORMS_FEEDBACK_ENTRY: text,
        'emailAddress': user_email,
    }

    try:
        response = await sync_to_async(requests.post)(
            settings.GOOGLE_FORMS_FORM_RESPONSE_URL,
            data=data, timeout=5,
        )

        if response.status_code not in {200, 302}:
            raise FeedbackSendError(f'Google Forms HTTP {response.status_code}')

    except Exception as exc:
        raise FeedbackSendError(str(exc)) from exc
