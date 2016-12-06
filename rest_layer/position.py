from flask_restful import Resource


class Position(Resource):
    def __init__(self, entry):
        self.entry = entry
    
    def get(self, position_id):
        #Perform query and return JSON data
        hour_data = entry.get_hour_info(position_id)
        return {'hour_data': hour_data}