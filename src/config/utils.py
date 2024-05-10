from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError) and 'detail' not in response.data:
            # This is a serializer validation error
            # Flatten the error messages into a single string
            message = ''
            for field, messages in response.data.items():
                message += f'{field}: {" ".join(messages)} '

            response.data = {'message': message.strip()}
        else:
            # For all other types of errors
            response.data = {'message': str(response.data['detail'])}

    return response
