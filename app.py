from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import markdown2

app = Flask(__name__)

@app.route('/')
def index():
    # Read the content of the README.md file
    with open('README.md', 'r') as file:
        readme_content = file.read()

    # Convert Markdown content to HTML
    html_content = markdown2.markdown(readme_content)

    # Render the HTML content
    return render_template('index.html', content=html_content)

app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

def serialize_hero(hero):
    return {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [
            {
                "id": hero_power.id,
                "hero_id": hero_power.hero_id,
                "power_id": hero_power.power_id,
                "strength": hero_power.strength,
                "power": serialize_power(hero_power.power)
            }
            for hero_power in hero.hero_powers
        ]
    }

def serialize_power(power):
    return {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }

def serialize_hero_power(hero_power):
    return {
        "id": hero_power.id,
        "hero_id": hero_power.hero_id,
        "power_id": hero_power.power_id,
        "strength": hero_power.strength,
        "hero": serialize_hero(hero_power.hero),
        "power": serialize_power(hero_power.power)
    }

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(serialize_hero(hero))
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([serialize_power(power) for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(serialize_power(power))
    else:
        return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.json
    if 'description' not in data:
        return jsonify({"error": "Description is required"}), 400

    description = data['description']
    if len(description) < 20:
        return jsonify({"error": "Description must be at least 20 characters long"}), 400

    power.description = description
    try:
        db.session.commit()
        return jsonify(serialize_power(power))
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Validation errors"}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    required_fields = ['strength', 'power_id', 'hero_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Required fields are missing"}), 400

    strength = data['strength']
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"error": "Invalid strength"}), 400

    hero_id = data['hero_id']
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    power_id = data['power_id']
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    try:
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(serialize_hero_power(hero_power))
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Validation errors"}), 400

if __name__ == '__main__':
    app.run(debug=True)
