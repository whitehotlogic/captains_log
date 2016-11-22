import json
from config.config_example import CONFIG as EXAMPLE_CONFIG


def run_setup():

    NEW_CONFIG = {}

    def get_response(key):
        try:
            response = raw_input("what is the {0}? ".format(key))
        except NameError:  # python 2/3 compatible
            response = input("what is the {0}? ".format(key))
        try:
            if type(EXAMPLE_CONFIG[key]) == int:
                response = int(response)
        except ValueError:
            print("An number value must be supplied. Try again: ")
            return get_response(key)
        NEW_CONFIG[key] = response

    for key in EXAMPLE_CONFIG:
        get_response(key)

    with open("config/config.py", "w") as file:
        file.write("CONFIG = " + str(json.dumps(
            NEW_CONFIG, sort_keys=True, indent=4, separators=(',', ': '))))
