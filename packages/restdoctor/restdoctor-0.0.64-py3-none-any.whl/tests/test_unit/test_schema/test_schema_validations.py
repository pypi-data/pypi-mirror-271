from __future__ import annotations

import pytest
from django.core.exceptions import ImproperlyConfigured
from rest_framework.fields import Field
from rest_framework.routers import SimpleRouter

from restdoctor.rest_framework.schema import RestDoctorSchema
from restdoctor.rest_framework.schema.generators import RefsSchemaGenerator30
from tests.stubs.serializers import MyModelWithoutHelpTextsSerializer, WithMethodFieldSerializer
from tests.test_unit.test_schema.conftest import UrlConf
from tests.test_unit.test_schema.stubs import DefaultViewSet, DefaultViewSetWithOperationId


@pytest.mark.parametrize(
    ('field', 'expected_help_text'), [(Field(), None), (Field(help_text='help_text'), 'help_text')]
)
def test_get_field_description_not_raises_success_case(field, expected_help_text):
    schema = RestDoctorSchema()

    result = schema.get_field_description(field)

    assert result == expected_help_text


def test_get_field_description_strict_fail_case(settings):
    settings.API_STRICT_SCHEMA_VALIDATION = True
    schema = RestDoctorSchema()

    with pytest.raises(ImproperlyConfigured):
        schema.get_field_description(Field())


def test_get_field_description_success_case(settings):
    settings.API_STRICT_SCHEMA_VALIDATION = True
    schema = RestDoctorSchema()

    result = schema.get_field_description(Field(help_text='help_text'))

    assert result == 'help_text'


def test_get_field_description_model_field_not_raises_success_case():
    schema = RestDoctorSchema()

    result = schema.get_field_description(
        MyModelWithoutHelpTextsSerializer().fields['abstract_field']
    )

    assert result is None


def test_get_field_description_model_field_strict_fail_case(settings):
    settings.API_STRICT_SCHEMA_VALIDATION = True
    schema = RestDoctorSchema()

    with pytest.raises(ImproperlyConfigured):
        schema.get_field_description(MyModelWithoutHelpTextsSerializer().fields['abstract_field'])


def test_get_field_description_model_field_success_case(settings):
    settings.API_STRICT_SCHEMA_VALIDATION = True
    schema = RestDoctorSchema()

    result = schema.get_field_description(MyModelWithoutHelpTextsSerializer().fields['timestamp'])

    assert result == 'Event timestamp'


@pytest.mark.parametrize(
    'field',
    [
        'field',
        'optional_field',
        'many_field',
        'list_field',
        'optional_many_field',
        'optional_list_field',
        'multiple_choice_field',
        'type_checking_field',
    ],
)
def test_check_annotations_success_case(settings, field):
    settings.API_STRICT_SCHEMA_VALIDATION = True
    schema = RestDoctorSchema()
    serializer = WithMethodFieldSerializer()

    schema.map_field(serializer.fields[field])


@pytest.mark.parametrize(
    'field',
    [
        'incorrect_field',
        'incorrect_optional_field',
        'incorrect_many_field',
        'incorrect_list_field',
        'incorrect_optional_many_field',
        'incorrect_multiple_choice_field',
    ],
)
def test_check_annotations_fail_case(settings, field):
    settings.API_STRICT_SCHEMA_VALIDATION = True
    schema = RestDoctorSchema()
    serializer = WithMethodFieldSerializer()

    with pytest.raises(ImproperlyConfigured):
        schema.map_field(serializer.fields[field])


def test_duplicate_operation_ids_fail_case(make_urlconf):
    urlconf = make_urlconf(('foo', DefaultViewSet, 'foo'), ('bar', DefaultViewSet, 'bar'))
    generator = RefsSchemaGenerator30(urlconf=urlconf)

    with pytest.raises(Exception, match='duplicates existing id'):
        generator.get_schema()


def test_duplicate_operation_ids_success_case(make_urlconf):
    urlconf = make_urlconf(
        ('foo', DefaultViewSet, 'foo'), ('bar', DefaultViewSetWithOperationId, 'bar')
    )
    generator = RefsSchemaGenerator30(urlconf=urlconf)

    schema = generator.get_schema()
    pass
