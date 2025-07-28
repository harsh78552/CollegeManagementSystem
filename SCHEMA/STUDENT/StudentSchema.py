from marshmallow import Schema, fields


class StudentRegisteration(Schema):
	name = fields.Str(required=True)
	contact = fields.Str(required=True)
	email = fields.Str(required=True)
	password = fields.Str(required=True)
	branch = fields.Str(required=True)
	registeration_no = fields.Str(required=True)
	year = fields.Str(required=True)
	semester = fields.Str(required=True)
	blood_group = fields.Str(required=True)
	address = fields.Str(required=True)
