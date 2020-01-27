import graphene
from django.core.exceptions import ValidationError

from examples.models import Location
from examples.schema import LocationNode
from graphene_validation.mutations import MutationWithValidators


class CreateLocationInput(graphene.InputObjectType):
    name = graphene.String()
    country = graphene.String()


class CreateLocation1(MutationWithValidators):
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

        return CreateLocation1(location)


class LocationValidators:
    @classmethod
    def validate_name(cls, info, **kwargs):
        location_data = kwargs.get("location_data")

        if not location_data["name"].isupper():
            raise ValidationError(
                "Location name have to starts with capital letters."
            )


class CreateLocation2(LocationValidators, MutationWithValidators):
    location = graphene.Field(LocationNode)

    class Arguments:
        location_data = CreateLocationInput(required=True)

    @classmethod
    def perform_mutate(cls, root, info, location_data):
        location = Location.objects.create(**location_data)

        return CreateLocation1(location)


class CreateLocation3(LocationValidators, MutationWithValidators):
    location = graphene.Field(LocationNode)

    class Meta:
        excluded_validators = ('validate_name', )

    class Arguments:
        location_data = CreateLocationInput(required=True)

    @classmethod
    def perform_mutate(cls, root, info, location_data):
        location = Location.objects.create(**location_data)

        return CreateLocation1(location)
