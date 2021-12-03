import random
import json
import os


"""
This should contain the processing detail, including assigning a result status, and the result detail to the submission
"""

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def randomStatus():
    """
    This function gives a random result(status) to a submission
    :return: status
    """
    resultSet = ["Success", "Pending", "Fail", "Warning"]
    result = random.choice(resultSet)
    return result

def demoResult():
    filepath = os.path.join(THIS_FOLDER, "../results/demo_result.json")
    f = open(filepath)
    data = json.dumps(json.load(f))
    return data

