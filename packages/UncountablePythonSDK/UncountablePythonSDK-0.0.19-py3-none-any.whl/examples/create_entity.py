from uncountable.core import AuthDetailsApiKey, Client
from uncountable.types import (
    entity_t,
    field_values_t,
)


client = Client(
    base_url="https://app.uncountable.com",
    auth_details=AuthDetailsApiKey(
        api_id="X",
        api_secret_key="X",
    ),
)
entities = client.create_entity(
    definition_id=24,
    entity_type=entity_t.EntityType.LAB_REQUEST,
    field_values=[
        field_values_t.FieldRefNameValue(
            field_ref_name="name", value="SDK Lab Request"
        ),
        field_values_t.FieldRefNameValue(field_ref_name="materialFamilyId", value=1),
    ],
)
print(entities)
