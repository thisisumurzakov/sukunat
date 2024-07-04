import random

from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
import importlib
from django.conf import settings


def get_sms_client():
    module_name, class_name = settings.SMS_CLIENT_CLASS.rsplit(".", 1)
    module = importlib.import_module(module_name)
    client_class = getattr(module, class_name)
    return client_class()


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError) and "detail" not in response.data:
            # This is a serializer validation error
            # Flatten the error messages into a single string
            message = ""
            for field, messages in response.data.items():
                message += f'{field}: {" ".join(messages)} '

            response.data = {"message": message.strip()}
        else:
            # For all other types of errors
            response.data = {"message": str(response.data["detail"])}

    return response


def get_random_color():
    colors = [
        "#81C784",
        "#64B5F6",
        "#FFB74D",
        "#4FC3F7",
        "#FF8A65",
        "#9575CD",
        "#4DB6AC",
        "#FFF176",
        "#AED581",
        "#BA68C8",
        "#FFD54F",
        "#4DD0E1",
        "#FFB74D",
        "#A1887F",
        "#90CAF9",
        "#F48FB1",
        "#81D4FA",
        "#B39DDB",
        "#E6EE9C",
        "#FFAB91",
    ]
    return random.choice(colors)
