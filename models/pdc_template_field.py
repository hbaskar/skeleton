from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime
from . import Base

class PdcTemplateField(Base):
    __tablename__ = 'pdc_template_fields'

    template_field_id = Column(Integer, primary_key=True, autoincrement=True)
    template_id = Column(Integer, ForeignKey('pdc_templates_test.template_id'), nullable=False)
    metadata_key = Column(String(100), nullable=False)
    display_name = Column(String(100))
    data_type = Column(String(50))
    is_required = Column(Boolean, default=False, nullable=False)
    default_value = Column(String(250))
    validation_rule = Column(String(250))
    sort_order = Column(Integer)
    lookup_type = Column(String(100))
    lookup_url = Column(String(500))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = Column(String(100), nullable=False)
    modified_at = Column(DateTime)
    modified_by = Column(String(100))

    def to_dict(self):
        return {
            'template_field_id': self.template_field_id,
            'template_id': self.template_id,
            'metadata_key': self.metadata_key,
            'display_name': self.display_name,
            'data_type': self.data_type,
            'is_required': self.is_required,
            'default_value': self.default_value,
            'validation_rule': self.validation_rule,
            'sort_order': self.sort_order,
            'lookup_type': self.lookup_type,
            'lookup_url': self.lookup_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None,
            'modified_by': self.modified_by
        }
