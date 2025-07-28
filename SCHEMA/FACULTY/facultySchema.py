from marshmallow import fields, Schema


class FacultyRegistrationSchema(Schema):
	name = fields.Str(required=True)
	contact = fields.Str(required=True)
	email = fields.Str(required=True)
	password = fields.Str(required=True)
	subject = fields.Str(required=True)
	qualification = fields.Str(required=True)
	role = fields.Str(required=True)
	blood_group = fields.Str(required=True)
