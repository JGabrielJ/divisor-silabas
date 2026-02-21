# divisor_app/services/exceptions.py

SITE_MESSAGES = {
    'email_success': 'Obrigado pelo seu feedback!',
    'not_authorized': 'Acesso não autorizado. Verifique suas credenciais.',
    'internal_error': 'Erro interno no processamento da solicitação. Tente novamente.',
    'unable_to_access': 'Não foi possível acessar a API. Tente novamente em instantes.',
    'unable_to_send': 'Não foi possível enviar o feedback no momento. Tente novamente mais tarde.',
}

class CoreAPIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.message = message
        self.status_code = status_code
        super().__init__(f'CoreAPIError {status_code}: {message}')

class FeedbackSendError(Exception):
    pass
