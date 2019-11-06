from django.contrib.auth import get_user_model
from django.apps import apps
from rest_framework.views import exception_handler
from .utils import ERROR_API

import math
import six
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import pagination


UserModel = get_user_model()
# CategoryModel = apps.get_model('common', 'Category')
# OfferModel = apps.get_model('yomarket', 'Offer')
# CompanyModel = apps.get_model('yomarket', 'Shop')


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


class CustomPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        self.page_size = page_size
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


    def get_next_page(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_page(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_page(),
                'previous': self.get_previous_page()
            },
            'items_count': self.page.paginator.count,
            'page_size': self.page_size,
            'pages_count': math.ceil(self.page.paginator.count / self.page_size),
            'results': data
        })


def prepare_paginated_response(obj, request, queryset):
    page_num = request.GET.get('page', None)
    if page_num:
        page = obj.paginate_queryset(queryset)
        if page is not None:
            serializer = obj.get_serializer(page, many=True, context={'request': request})
            paginated_response = obj.get_paginated_response(serializer.data)
            content = paginated_response.data['results']
            del paginated_response.data['results']
            metadata = paginated_response.data

            paginated = type('PaginatedData', (object,), {})
            paginated.content = content
            paginated.metadata = metadata
            return paginated
    return None


