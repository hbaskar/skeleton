from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime
from models.pdc_template import PdcTemplate, Base

class PdcClass(Base):
    __tablename__ = 'pdc_class_test'

    class_id = Column(Integer, primary_key=True, autoincrement=True)
    template_id = Column(Integer, ForeignKey('pdc_templates_test.template_id'), nullable=False)
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

    @staticmethod
    def from_template_and_data(template_obj, data_dict):
        """
        Create a dict of model fields from a template object and incoming data dict.
        data_dict: {template_attr_name: value, ...}
        """
        # Build mapping: template_attr_name -> attribute_X
        attr_map = {}
        for i in range(1, 36):
            template_attr = getattr(template_obj, f"attribute_{i}")
            if template_attr:
                attr_map[template_attr] = f"attribute_{i}"
        # Prepare kwargs for model fields
        model_kwargs = {}
        for k, v in data_dict.items():
            field = attr_map.get(k)
            if field:
                model_kwargs[field] = v
        # Add other required fields (template_id, name, etc.) in the service/endpoint
        return model_kwargs

    def to_dict(self, template_obj=None):
        # If template_obj is not provided, fallback to attribute_1, attribute_2, ...
        if template_obj:
            attr_names = [getattr(template_obj, f'attribute_{i}') or f'attribute_{i}' for i in range(1, 36)]
        else:
            attr_names = [f'attribute_{i}' for i in range(1, 36)]
        attributes = {attr_names[i]: getattr(self, f'attribute_{i+1}') for i in range(35)}
        return {
            'class_id': self.class_id,
            'template_id': self.template_id,
            'name': self.name,
            'attributes': attributes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by,
            'is_active': self.is_active
        }
