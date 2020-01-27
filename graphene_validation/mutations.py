from collections import OrderedDict

from django.core.exceptions import ValidationError
from graphene import Interface, Field, ObjectType
from graphene.types.mutation import MutationOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene.utils.props import props


class MutationWithValidatorsOptions(MutationOptions):
    excluded_validators = None


class MutationWithValidators(ObjectType):
    """
    Mutation that calls all validation methods before performing mutate.

    Validation method name have to starts with 'validate_' to be called,
    if validation fails methods have to raise ValidationError.

    To exclude some validation methods, pass them as list / tuple
    to the excluded_validators.
    """
    @classmethod
    def __init_subclass_with_meta__(
        cls,
        interfaces=(),
        resolver=None,
        output=None,
        arguments=None,
        excluded_validators=None,
        _meta=None,
        **options
    ):
        if not _meta:
            _meta = MutationWithValidatorsOptions(cls)

        output = output or getattr(cls, "Output", None)
        fields = {}

        for interface in interfaces:
            assert issubclass(interface, Interface), (
                "All interfaces of {} must be a subclass of Interface. "
                'Received "{}".'
            ).format(cls.__name__, interface)
            fields.update(interface._meta.fields)

        if not output:
            fields = OrderedDict()
            for base in reversed(cls.__mro__):
                fields.update(yank_fields_from_attrs(base.__dict__, _as=Field))
            output = cls

        if not arguments:
            input_class = getattr(cls, "Arguments", None)

            if input_class:
                arguments = props(input_class)
            else:
                arguments = {}

        if _meta.fields:
            _meta.fields.update(fields)
        else:
            _meta.fields = fields

        _meta.interfaces = interfaces
        _meta.output = output
        _meta.resolver = cls._mutate
        _meta.arguments = arguments
        _meta.excluded_validators = excluded_validators

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def _mutate(cls, root, info, **kwargs):
        perform_mutate = getattr(cls, "perform_mutate", None)

        not_implemented_message = (
            "MutationWithValidators must define a perform_mutate method in it"
        )

        assert perform_mutate, not_implemented_message

        if not cls._meta.excluded_validators:
            excluded_validators = []
        else:
            excluded_validators = cls._meta.excluded_validators

        validate_methods = [
            getattr(cls, m)
            for m in dir(cls)
            if m.startswith("validate_") and m not in excluded_validators
        ]

        errors = []
        for method in validate_methods:
            try:
                method(info, **kwargs)
            except ValidationError as e:
                errors.append(e.message)

        if errors:
            # TODO: find a better way to display errors
            raise GraphQLError(", ".join(errors))

        return perform_mutate(root, info, **kwargs)

    @classmethod
    def Field(
        cls, name=None, description=None, deprecation_reason=None, required=False,
    ):
        return Field(
            cls._meta.output,
            args=cls._meta.arguments,
            resolver=cls._meta.resolver,
            name=name,
            description=description or cls._meta.description,
            deprecation_reason=deprecation_reason,
            required=required,
        )
