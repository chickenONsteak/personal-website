from marshmallow import Schema, fields, validate, EXCLUDE

class AddOneProject(Schema):
    class Meta:
        unknown = EXCLUDE
    date = fields.Date(required=True)
    title = fields.Str(validate=validate.Length(min=1, error='Title has to be at least 1 character long.'),
                       required=True)
    tag = fields.Str(validate=validate.Length(min=1, error='Tag has to be at least 1 character long.'),
                     required=True)
    description = fields.Str(validate=validate.Length(min=1, error='Description has to be at least 1 character long.'),
                             required=True)