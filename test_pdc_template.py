import pytest
from services.pdc_template_service import (
    create_template, get_template, list_templates, update_template, delete_template
)

def test_create_and_get_template():
    data = {
        'name': 'Test Template',
        'attributes': ['A1', 'A2'] + [None]*33,
        'created_by': 'tester',
        'is_active': True
    }
    template = create_template(data)
    assert template.template_id is not None
    fetched = get_template(template.template_id)
    assert fetched.name == 'Test Template'
    assert fetched.attribute_1 == 'A1'
    assert fetched.attribute_2 == 'A2'
    assert fetched.created_by == 'tester'
    assert fetched.is_active is True

def test_update_template():
    data = {
        'name': 'Update Test',
        'attributes': ['B1', 'B2'] + [None]*33,
        'created_by': 'tester',
        'is_active': True
    }
    template = create_template(data)
    update_data = {
        'name': 'Updated Name',
        'attributes': ['C1', 'C2'] + [None]*33,
        'updated_by': 'updater',
        'is_active': False
    }
    updated = update_template(template.template_id, update_data)
    assert updated.name == 'Updated Name'
    assert updated.attribute_1 == 'C1'
    assert updated.attribute_2 == 'C2'
    assert updated.updated_by == 'updater'
    assert updated.is_active is False

def test_list_templates():
    templates = list_templates()
    assert isinstance(templates, list)
    assert len(templates) >= 1

def test_delete_template():
    data = {
        'name': 'Delete Test',
        'attributes': ['D1', 'D2'] + [None]*33,
        'created_by': 'tester',
        'is_active': True
    }
    template = create_template(data)
    deleted = delete_template(template.template_id)
    assert deleted is True
    assert get_template(template.template_id) is None
