import random


"""
This should contain the processing detail, including assigning a result status, and the result detail to the submission
"""

def randomStatus():
    """
    This function gives a random result(status) to a submission
    :return: status
    """
    resultSet = ["Success", "Pending", "Fail", "Warning"]
    result = random.choice(resultSet)
    return result
