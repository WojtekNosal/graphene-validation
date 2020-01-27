from graphene import relay

from examples.models import Location
from graphene_django import DjangoObjectType


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location
        filter_fields = ["country"]
        interfaces = (relay.Node,)
