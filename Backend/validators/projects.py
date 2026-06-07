from marshmallow import Schema, fields, validate, EXCLUDE

class AddOneProject(Schema):
    class Meta:
        unknown = EXCLUDE
    title = fields.Str(validate=validate.Length(min=1, error='Title has to be at least 1 character long.'),
                       required=True)
    completed_date = fields.Date(required=True)
    categories = fields.Str(validate=validate.Length(min=1, error='Project should have at least 1 category.'),
                     required=True)
    description = fields.Str(validate=validate.Length(min=1, error='Description has to be at least 1 character long.'),
                             required=True)
    image_urls = fields.Str(validate=validate.Length(min=1, error='You have to include at least 1 image'),
                             required=True)