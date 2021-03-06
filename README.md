## Graphene Custom Mutation with validation

Custom Graphene Mutation that calls defined validation methods before performing mutate.

Custom Validator name have to starts with **'validate\_'**, 
if validation fails method have to raise Validation Error with proper message.

## Example

```python
class CreateLocationInput(graphene.InputObjectType):
    name = graphene.String()
    country = graphene.String()


class CreateLocation(MutationWithValidators):
    location = graphene.Field(LocationNode)

    class Arguments:
        location_data = CreateLocationInput(required=True)

    @classmethod
    def validate_name(cls, info, **kwargs):
        location_data = kwargs.get("location_data")

        if not location_data["name"].isupper():
            raise ValidationError(
                "Location name have to starts with capital letters."
            )

    @classmethod
    def perform_mutate(cls, root, info, location_data):
        location = Location.objects.create(**location_data)

        return CreateLocation(location)
```

If we try to send location name in lowercase, response will look like this:

```json
{
  "errors": [
    {
      "message": "Location name have to starts with capital letters.",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": [
        "createLocation"
      ]
    }
  ],
  "data": {
    "createLocation": null
  }
}
```

Or validators can be defined in separate class:

```python
class LocationValidators:
    @classmethod
    def validate_name(cls, info, **kwargs):
        location_data = kwargs.get("location_data")

        if not location_data["name"].isupper():
            raise ValidationError(
                "Location name have to starts with capital letters."
            )


class CreateLocation(LocationValidators, MutationWithValidators):
    location = graphene.Field(LocationNode)

    # to exclude some validators just pass them to excluded_validators
    class Meta:
        excluded_validators = ('validate_name', )
```

## Work in progress
need to add tests, better error handling and much more...
