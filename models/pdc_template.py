from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from . import Base

class PdcTemplate(Base):
    __tablename__ = 'pdc_templates_test'

    template_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    attribute_1 = Column(String(250))
    attribute_2 = Column(String(250))
    attribute_3 = Column(String(250))
    attribute_4 = Column(String(250))
    attribute_5 = Column(String(250))
    attribute_6 = Column(String(250))
    attribute_7 = Column(String(250))
    attribute_8 = Column(String(250))
    attribute_9 = Column(String(250))
    attribute_10 = Column(String(250))
    attribute_11 = Column(String(250))
    attribute_12 = Column(String(250))
    attribute_13 = Column(String(250))
    attribute_14 = Column(String(250))
    attribute_15 = Column(String(250))
    attribute_16 = Column(String(250))
    attribute_17 = Column(String(250))
    attribute_18 = Column(String(250))
    attribute_19 = Column(String(250))
    attribute_20 = Column(String(250))
    attribute_21 = Column(String(250))
    attribute_22 = Column(String(250))
    attribute_23 = Column(String(250))
    attribute_24 = Column(String(250))
    attribute_25 = Column(String(250))
    attribute_26 = Column(String(250))
    attribute_27 = Column(String(250))
    attribute_28 = Column(String(250))
    attribute_29 = Column(String(250))
    attribute_30 = Column(String(250))
    attribute_31 = Column(String(250))
    attribute_32 = Column(String(250))
    attribute_33 = Column(String(250))
    attribute_34 = Column(String(250))
    attribute_35 = Column(String(250))
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = Column(String(100))
    updated_at = Column(DateTime)
    updated_by = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False)

    def to_dict(self):
        attributes = {}
        for i in range(1, 36):
            attr_name = f'attribute_{i}'
            val = getattr(self, attr_name)
            if val is not None:
                attributes[attr_name] = val
        return {
            'template_id': self.template_id,
            'name': self.name,
            'attributes': attributes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by,
            'is_active': self.is_active
        }
