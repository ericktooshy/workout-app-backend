from app import app
from models import db, Workout, Exercise, workout_exercise

with app.app_context():
    print("Deleting existing data...")
    db.session.execute(workout_exercise.delete())
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Creating Exercises...")
    bench_press = Exercise(name="Bench Press", target_muscle="Chest")
    squat = Exercise(name="Barbell Squat", target_muscle="Legs")
    pull_up = Exercise(name="Pull Up", target_muscle="Back")
    db.session.add_all([bench_press, squat, pull_up])
    db.session.commit()

    print("Creating Workouts...")
    push_day = Workout(name="Upper Body Push", date="2023-11-01")
    leg_day = Workout(name="Lower Body Power", date="2023-11-02")
    db.session.add_all([push_day, leg_day])
    db.session.commit()

    print("Adding Exercises to Workouts...")
    db.session.execute(workout_exercise.insert().values(workout_id=push_day.id, exercise_id=bench_press.id, sets=4, reps=8))
    db.session.execute(workout_exercise.insert().values(workout_id=leg_day.id, exercise_id=squat.id, sets=5, reps=5))
    db.session.commit()

    print("Seeding Complete!")