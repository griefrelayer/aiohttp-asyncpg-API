from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy_serializer import SerializerMixin
from marshmallow import Schema, fields, validates, ValidationError
from re import fullmatch

Base = declarative_base()


class Employees(Base, SerializerMixin):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    hire_date = Column(Date, nullable=False)


class EmployeeCreateSchema(Schema):
    id = fields.Integer(required=False)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    birth_date = fields.Date(format='%Y-%m-%d', required=True)
    hire_date = fields.Date(format='%Y-%m-%d', required=True)

    @validates('first_name')
    def validate_first_name(self, data, **kwargs):
        if not fullmatch(r'[\w]+', data):
            raise ValidationError("wrong first_name!")

    @validates('last_name')
    def validate_last_name(self, data, **kwargs):
        if not fullmatch(r'[\w]+', data):
            raise ValidationError("wrong last_name!")


class EmployeeUpdateSchema(Schema):
    id = fields.Integer(required=False)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    birth_date = fields.Date(format='%Y-%m-%d', required=False)
    hire_date = fields.Date(format='%Y-%m-%d', required=False)

    @validates('first_name')
    def validate_first_name(self, data, **kwargs):
        if not fullmatch(r'[\w]+', data):
            raise ValidationError("wrong first_name!")

    @validates('last_name')
    def validate_last_name(self, data, **kwargs):
        if not fullmatch(r'[\w]+', data):
            raise ValidationError("wrong last_name!")

