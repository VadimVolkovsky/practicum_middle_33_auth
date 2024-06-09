from pydantic import BaseModel, ConfigDict, UUID4


class RoleSerializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    name: str
