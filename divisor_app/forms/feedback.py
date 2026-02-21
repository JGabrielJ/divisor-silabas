# divisor_app/forms/feedback.py

from django import forms

class FeedbackForm(forms.Form):
    email = forms.EmailField(
        label='Informe seu e-mail', max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control mt-2'}),
    )

    feedback = forms.CharField(
        label='Críticas, problemas na busca ou erros na divisão? Descreva sua situação no campo abaixo 😊',
        min_length=1, max_length=100000, help_text='Forneça o máximo de detalhes possível.',
        widget=forms.Textarea(attrs={'class': 'form-control mt-2', 'rows': 4}),
    )
