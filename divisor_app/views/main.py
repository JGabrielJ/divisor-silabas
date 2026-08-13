#! divisor_app/views/main.py

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from requests import RequestException

from ..forms.word import WordForm
from ..services.core_api import CoreAPIClient
from ..services.exceptions import SITE_MESSAGES, CoreAPIError


def main_view(request):
    word_form = WordForm(request.POST or None)
    result = request.session.pop("result", None)

    hidden_fields = []
    if isinstance(result, dict):
        hidden_fields = [
            name for name in settings.PREMIUM_FIELDS if not result.get(name)
        ]

    if request.method == "POST":
        if word_form.is_valid():
            try:
                client = CoreAPIClient()
                result = client.analyze_word(word_form.cleaned_data["word"])
                request.session["result"] = result

            except CoreAPIError as exc:
                if exc.status_code == 418:
                    messages.info(request, exc.message)
                elif exc.status_code == 400:
                    messages.warning(request, exc.message)
                elif exc.status_code in {404, 422, 429}:
                    messages.error(request, exc.message)
                elif exc.status_code in {401, 403}:
                    messages.error(request, SITE_MESSAGES["not_authorized"])
                else:
                    messages.error(request, SITE_MESSAGES["internal_error"])

            except RequestException:
                messages.error(request, SITE_MESSAGES["unable_to_access"])

            except Exception:  # noqa: BLE001
                messages.error(request, SITE_MESSAGES["internal_error"])

        elif errors := word_form.errors.get("word"):
            code = errors.as_data()[0].code
            message = str(errors[0])

            if code:
                getattr(messages, code)(request, message)

        else:
            messages.error(request, SITE_MESSAGES["internal_error"])

        return redirect("main-view")

    return render(
        request,
        "divisor_app/index.html",
        {
            "word_form": word_form,
            "result": result,
            "hidden_fields": hidden_fields,
        },
    )
