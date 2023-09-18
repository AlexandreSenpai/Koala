import sys
from typing import TypedDict

sys.path.insert(0, '../')

import pytest
from datetime import datetime, timedelta
from koala.domain.entities.base import Entity

def test_should_auto_set_properties_if_instantiate_empty() -> None:
    entity = Entity()
    assert entity.id is not None
    assert isinstance(entity.created_at, datetime)
    assert isinstance(entity.updated_at, datetime)

def test_should_not_auto_set_properties_if_it_was_passed_at_instatiation() -> None:
    date = datetime.utcnow()
    entity = Entity(id='1',
                    created_at=date,
                    updated_at=date)
    assert entity.id == '1'
    assert entity.created_at == date
    assert entity.updated_at == date

def test_to_dict_should_return_class_props_as_dict() -> None:
    class ReturnObj(TypedDict):
        id: str
        created_at: datetime
        updated_at: datetime
    
    date = datetime.utcnow()
    entity = Entity[ReturnObj](id='1',
                    created_at=date,
                    updated_at=date)
    
    obj = entity.to_dict()

    assert isinstance(obj, dict) == True

    assert obj.get('id') == '1'
    assert obj.get('created_at') == date
    assert obj.get('updated_at') == date

def test_id_type_validation():
    # Test integer ID
    entity = Entity(id=1)
    assert isinstance(entity.id, int)

    # Test string ID
    entity = Entity(id="1")
    assert isinstance(entity.id, str)

    # Test invalid ID type
    with pytest.raises(Exception, match='Id must be an str or int value.'):
        Entity(id=1.0)

def test_datetime_update():
    entity = Entity()
    original_updated_at = entity.updated_at

    # Simulate an update by changing the updated_at attribute
    new_updated_at = original_updated_at + timedelta(days=1)
    entity.updated_at = new_updated_at

    assert entity.updated_at == new_updated_at

def test_datetime_immutability():
    with pytest.raises(Exception):
        entity = Entity()
        original_created_at = entity.created_at

        # Try to change the created_at attribute
        new_created_at = original_created_at + timedelta(days=1)
        entity.created_at = new_created_at


def test_to_dict_with_empty_object():
    entity = Entity()
    entity_dict = entity.to_dict()
    assert 'id' in entity_dict
    assert 'created_at' in entity_dict
    assert 'updated_at' in entity_dict