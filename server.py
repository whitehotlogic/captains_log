from flask import Flask
from flask_restful import Resource, Api
from rest_layer.day import Day
from rest_layer.position import Position
from model.entry import Entry

entry = Entry('test.db')

app = Flask(__name__)
api = Api(app)

api.add_resource(Position, '/position/<string:position_id>', resource_class_kwargs={'entry': entry})
api.add_resource(Day, '/day/<int:day_id>', resource_class_kwargs={'entry': entry})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

