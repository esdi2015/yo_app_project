from django.contrib.auth import get_user_model
from django.apps import apps
from rest_framework.views import exception_handler
from .utils import ERROR_API


UserModel = get_user_model()
CategoryModel = apps.get_model('common', 'Category')
OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    api_error_codes = []
    metadata = {}
    response = exception_handler(exc, context)
    try:
        detail = response.data.get('detail')
    except Exception as e:
        detail = e
    if response is not None:
        if detail:
            if detail == ERROR_API['118'][1]:
                api_error_codes.append(ERROR_API['118'][0])
            elif detail == ERROR_API['119'][1]:
                api_error_codes.append(ERROR_API['119'][0])
            #else:
            metadata = {'api_error_codes': api_error_codes}
            response.data['metadata'] = metadata
            response.data['errors'] = {'non_field_errors': detail}
            del response.data['detail']

    return response


def custom_api_response(serializer=None, content=None, errors=None, metadata={}, error_codes=[]):
    api_error_codes = []
    if content:
        response = {'metadata': metadata, 'content': content}
        return response

    if errors:
        if len(error_codes) > 0:
            metadata = {'api_error_codes': error_codes}
        response = {'metadata': metadata, 'errors': errors}
        return response

    if not hasattr(serializer, '_errors') or len(serializer._errors) == 0:
        if hasattr(serializer, 'data'):
            response = {'metadata': metadata, 'content': serializer.data}
        else:
            response = {'metadata': metadata, 'content': 'unknown'}
    else:
        for key in serializer._errors.keys():
            if key == 'password':
                for i, pe in enumerate(serializer._errors[key]):
                    if pe == ERROR_API['151'][1]:
                        serializer._errors[key][i].code = ERROR_API['151'][0]
                    elif pe == ERROR_API['152'][1]:
                        serializer._errors[key][i].code = ERROR_API['152'][0]
                    elif pe == ERROR_API['153'][1]:
                        serializer._errors[key][i].code = ERROR_API['153'][0]
                    api_error_codes.append(serializer._errors[key][i].code)
            elif key == 'photo':
                for i, pe in enumerate(serializer._errors[key]):
                    if pe == ERROR_API['161'][1]:
                        serializer._errors[key][i].code = ERROR_API['161'][0]
                    api_error_codes.append(serializer._errors[key][i].code)
            elif key == 'date_birth':
                for i, pe in enumerate(serializer._errors[key]):
                    if pe == ERROR_API['162'][1]:
                        serializer._errors[key][i].code = ERROR_API['162'][0]
                    api_error_codes.append(serializer._errors[key][i].code)
            else:
                try:
                    api_error_codes.append(serializer._errors[key][0].code)
                except Exception as e:
                    pass

        if len(api_error_codes) > 0:
            metadata = {'api_error_codes': api_error_codes}
        response = {'metadata': metadata, 'errors': serializer._errors}
    return response



def password_error_messages(serializer, key):
    for i, pe in enumerate(serializer._errors[key]):
        if pe == ERROR_API['151'][1]:
            serializer._errors[key][i].code = ERROR_API['151'][0]
        elif pe == ERROR_API['152'][1]:
            serializer._errors[key][i].code = ERROR_API['152'][0]
        elif pe == ERROR_API['153'][1]:
            serializer._errors[key][i].code = ERROR_API['153'][0]
    return serializer


def get_error_code():
    return None






