from pydantic import BaseModel, ConfigDict


class RoleCreateSerializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class RoleSerializer(RoleCreateSerializer):
    id: int


class AssignRoleSerializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    role: RoleSerializer
