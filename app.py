from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Workout, Exercise, workout_exercise
from schemas import workout_schema, workouts_schema, exercise_schema, exercises_schema
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# ----------------- WORKOUT ENDPOINTS -----------------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.jsonify(workouts), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        new_workout = Workout(name=data['name'], date=data['date'])
        db.session.add(new_workout)
        db.session.commit()
        return workout_schema.jsonify(new_workout), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.jsonify(workout), 200

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200

# ----------------- EXERCISE ENDPOINTS -----------------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.jsonify(exercises), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        new_exercise = Exercise(name=data['name'], target_muscle=data['target_muscle'])
        db.session.add(new_exercise)
        db.session.commit()
        return exercise_schema.jsonify(new_exercise), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.jsonify(exercise), 200

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted successfully"}), 200

# ------------- ADD EXERCISE TO WORKOUT -------------

@app.route('/workouts/<int:workout_id>/exercises', methods=['POST'])
def add_exercise_to_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    
    data = request.json
    exercise_id = data.get('exercise_id')
    sets = data.get('sets')
    reps = data.get('reps')

    if not all([exercise_id, sets, reps]):
        return jsonify({"error": "exercise_id, sets, and reps are required"}), 400

    exercise = Exercise.query.get_or_404(exercise_id)

    # Insert into the association table
    stmt = workout_exercise.insert().values(
        workout_id=workout.id, 
        exercise_id=exercise.id, 
        sets=sets, 
        reps=reps
    )
    
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify({"message": f"Added {exercise.name} to {workout.name}"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database constraint failed. Ensure sets and reps are > 0."}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)