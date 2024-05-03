from pydantic import BaseModel


class BaseRequest(BaseModel):
    """Base class for API requests."""

    @classmethod
    def examples(cls):
        field_values = {}
        for name, field in cls.model_fields.items():
            default_value = field.default
            field_values[name] = default_value
            if field.examples is not None:
                if len(field.examples) > 0:
                    field_values[name] = field.examples[0]
        return cls(**field_values)
