from flask_restful import Resource


class Day(Resource):
    def __init__(self, entry):
        self.entry = entry

    def get(self, day_id):
        #Perform query and return JSON data
        day_data = self.entry.get_day_info(day_id)
        return {'day_data': day_data}
