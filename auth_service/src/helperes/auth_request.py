from fastapi import Request

from src.api.v1.serializers.role_serializer import AssignRoleSerializer


class AuthRequest(Request):
    request_user: AssignRoleSerializer
