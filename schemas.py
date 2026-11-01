from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    # SCHEMA VALIDATION 1: Length enforcement on creation
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    target_muscle = fields.Str(required=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    date = fields.Str(required=True)
    
    # Nested serialization to show exercises inside a workout
    exercises = fields.Nested(ExerciseSchema, many=True, dump_only=True)

    # SCHEMA VALIDATION 2: Custom date format validation (YYYY-MM-DD)
    @validates('date')
    def validate_date_format(self, value):
        if len(value) != 10 or value[4] != '-' or value[7] != '-':
            raise ValidationError("Date must be in YYYY-MM-DD format.")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)