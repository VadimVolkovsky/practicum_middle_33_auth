from fastapi import Request

from api.v1.serializers.role_serializer import AssignRoleSerializer


class AuthRequest(Request):
    request_user: AssignRoleSerializer
