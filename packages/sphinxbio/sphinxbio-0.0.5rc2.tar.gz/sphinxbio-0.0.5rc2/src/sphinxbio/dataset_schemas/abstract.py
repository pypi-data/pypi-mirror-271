import pydantic

Field = pydantic.Field
model_validator = pydantic.model_validator
SphinxModel = pydantic.BaseModel


class AbstractSphinxDatasetSchema(SphinxModel):
    pass
