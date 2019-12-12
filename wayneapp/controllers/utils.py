from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from wayneapp.constants import ControllerConstants


class ControllerUtils:

    @staticmethod
    def unauthorized_response() -> Response:
        return ControllerUtils.custom_response(
            ControllerConstants.UNAUTHORIZED,
            status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def business_entity_not_exist_response(business_entity: str) -> Response:
        return ControllerUtils.custom_response(
            ControllerConstants.BUSINESS_ENTITY_NOT_EXIST.format(business_entity),
            status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def custom_response(message: str, status_code: status) -> Response:
        return Response(
            {
                "message": message
            },
            status=status_code
        )
    
    @staticmethod
    def extract_body(request: Request) -> dict:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        return body

    @staticmethod
    def add_permission_string(business_entity: str) -> str:
        return ControllerConstants.ADD +\
               ControllerConstants.UNDERSCORE +\
               ControllerUtils.remove_underscores(business_entity)

    @staticmethod
    def change_permission_string(business_entity: str) -> str:
        return ControllerConstants.CHANGE + \
               ControllerConstants.UNDERSCORE + \
               ControllerUtils.remove_underscores(business_entity)

    @staticmethod
    def delete_permission_string(business_entity: str) -> str:
        return ControllerConstants.DELETE + \
               ControllerConstants.UNDERSCORE + \
               ControllerUtils.remove_underscores(business_entity)

    @staticmethod
    def remove_underscores(string: str) -> str:
        return string.replace('_', '')
