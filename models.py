from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

# Association Table for Many-to-Many Relationship
workout_exercise = db.Table(
    'workout_exercise',
    db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id'), primary_key=True),
    # TABLE CONSTRAINTS: sets and reps must be positive integers
    db.Column('sets', db.Integer, CheckConstraint('sets > 0'), nullable=False),
    db.Column('reps', db.Integer, CheckConstraint('reps > 0'), nullable=False)
)

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    # TABLE CONSTRAINT: name and date cannot be null
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)

    # RELATIONSHIP: Many-to-Many
    exercises = db.relationship('Exercise', secondary=workout_exercise, back_populates='workouts')

    # MODEL VALIDATION 1: Ensure workout name is descriptive
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError("Workout name must be at least 3 characters long.")
        return name

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    # TABLE CONSTRAINT: Exercise name must be unique and cannot be null
    name = db.Column(db.String(100), unique=True, nullable=False)
    target_muscle = db.Column(db.String(50), nullable=False)

    # RELATIONSHIP: Many-to-Many
    workouts = db.relationship('Workout', secondary=workout_exercise, back_populates='exercises')

    # MODEL VALIDATION 2: Ensure target_muscle belongs to an approved list
    @validates('target_muscle')
    def validate_target_muscle(self, key, target_muscle):
        valid_muscles = ['Chest', 'Back', 'Legs', 'Arms', 'Core', 'Full Body']
        if target_muscle not in valid_muscles:
            raise ValueError(f"Target muscle must be one of: {', '.join(valid_muscles)}")
        return target_muscle