from pydantic import BaseModel, ConfigDict


class RoleCreateSerializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class RoleSerializer(RoleCreateSerializer):
    model_config = ConfigDict(from_attributes=True)

    id: int
