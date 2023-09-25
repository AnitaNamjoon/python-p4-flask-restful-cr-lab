#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    price = db.Column(db.Float)


@app.route('/plants', methods=['POST'])
def create_plant():
    
    data = request.get_json()

  
    if 'name' not in data or 'image' not in data or 'price' not in data:
        return make_response(jsonify({'error': 'Missing required data'}), 400)

    
    new_plant = Plant(
        name=data['name'],
        image=data['image'],
        price=data['price']
    )

    try:
        
        db.session.add(new_plant)
        db.session.commit()

        response = {
            'id': new_plant.id,
            'name': new_plant.name,
            'image': new_plant.image,
            'price': float(new_plant.price)
        }
        return jsonify(response), 201
    except Exception as e:
        
        db.session.rollback()
        return jsonify({'error': 'Error creating plant'}), 500



if __name__ == '__main__':
    app.run(port=5555, debug=True)
