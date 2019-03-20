from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'visitors.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# TODO: To create the database
'''
Use following code in python interactive shell

from crud import db
 db.create_all()

'''
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False)
    company = db.Column(db.String(120), unique=False)

    def __init__(self, name, company):
        self.name = name
        self.company = company

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'company')

visitor_schema = UserSchema()
visitors_schema = UserSchema(many=True)

# endpoint to create new user
@app.route("/visitor", methods=["POST"])
def add_user():
    name = request.json['name']
    company = request.json['company']
    
    new_visitor = Visitor(name, company)

    db.session.add(new_visitor)
    db.session.commit()

    return jsonify(new_visitor)

# endpoint to show all users
@app.route("/visitor", methods=["GET"])
def get_user():
    all_visitors = Visitor.query.all()
    result = visitors_schema.dump(all_visitors)
    return jsonify(result.data)

# endpoint to get user detail by id
@app.route("/visitor/<id>", methods=["GET"])
def visitor_detail(id):
    visitor = Visitor.query.get(id)
    return visitor_schema.jsonify(visitor)

# endpoint to update user
@app.route("/visitor/<id>", methods=["PUT"])
def visitor_update(id):
    visitor = visitor.query.get(id)
    name = request.json['name']
    company = request.json['company']

    visitor.company = company
    visitor.name = name

    db.session.commit()
    return user_schema.jsonify(visitor)

# # endpoint to delete user
# @app.route("/user/<id>", methods=["DELETE"])
# def user_delete(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()

#     return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)