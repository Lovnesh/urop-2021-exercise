from typing import Dict
from ga.chromosome_elem import ChromosomeElem
from routingTable import ROUTING_TABLE
from typing import List
from config import CHROMOSOME_LENGTH
import math
import random

coordinates = {}  # Used to keep track of the points in the abstract plane


def isLooping(checkedPoint: Dict[float, List[float]]) -> bool:
    '''
    Checks if the point that is to be plotted results in a loop around the track

    Parameters
    ----------
    checkedPoint: Dict[float, float]
        The points to be tallied against the ones plotted in the abstract plane so far
        The x-coordinate values are mapped to the y-coordinates value that have the same x-coordinate

    Returns
    -------
    Boolean :
        True, if the point results in the loop. False, otherwise.
    '''
    if len(checkedPoint) == 0 or len(coordinates) == 0:
        return False
    else:
        for key in checkedPoint:
            x_sim = coordinates.get(key)
            if x_sim:
                for i in checkedPoint[key]:
                    if i in x_sim:
                        return True
        return False


def merge_points(nonLoopingPoints: Dict[float, List[float]]):
    for key in nonLoopingPoints:
        abscissa = coordinates.get(key)
        if abscissa:
            for i in nonLoopingPoints[key]:
                abscissa.append(i)
        else:
            coordinates[key] = []
            abscissa = coordinates.get(key)
            for i in nonLoopingPoints[key]:
                abscissa.append(i)


def next_command(instructionNumber, previousCommand):
    if instructionNumber == 0 or instructionNumber == CHROMOSOME_LENGTH - 1:
        return ROUTING_TABLE[4]
    elif instructionNumber == CHROMOSOME_LENGTH - 2:
        if previousCommand == ROUTING_TABLE[3]:
            return ROUTING_TABLE[int(random.uniform(1.0,2.0))]
        else:
            return ROUTING_TABLE[4]
    else:
        if previousCommand == ROUTING_TABLE[3]:
            return ROUTING_TABLE[int(random.uniform(1.0, 2.0))]
        else:
            return ROUTING_TABLE[int(random.uniform(3.0, 4.0))]


def next_value(previousValue, currentCommand, previousCommand = None):
    fullCircle = 360.0
    if currentCommand == ROUTING_TABLE[4]:
        return random.randint(1,20)
    elif currentCommand == ROUTING_TABLE[3]:
        return random.uniform(1.0, 20.0)
    else:
        return random.randint(1, 
            math.floor(fullCircle/previousValue) - 1)


def generate_instructions() -> List[ChromosomeElem]:
    previousCommand = None
    previousValue = None
    x_coord = 0.0
    y_coord = 0.0
    totalAngle = 0.0 #Going Straight 
    currentCommand = None
    currentValue = None
    angleDY = 0.0
    ins_generated = 0
    instructionsList = []
    while ins_generated < CHROMOSOME_LENGTH:
        # Generate instructions and append it to the list
        while True:
            currentCommand = next_command(ins_generated, previousCommand)
            currentValue = next_value(previousValue, currentCommand, previousCommand)
            temp_x, temp_y = x_coord, y_coord
            points = {}
            if currentCommand == ROUTING_TABLE[3]:
                angleDY = currentValue
            elif currentCommand == ROUTING_TABLE[1] or currentCommand == ROUTING_TABLE[2]:
                i = 0
                while i < currentValue:
                    totalAngle += angleDY
                    temp_x, temp_y = point_storing(temp_x, temp_y, totalAngle, points)
                    i += 1
            else:
                i = 0
                while i < currentValue:
                    temp_x, temp_y = point_storing(temp_x, temp_y, totalAngle, points)
                    i += 1
            if not isLooping(points):
                merge_points(points)
                x_coord, y_coord = temp_x, temp_y
                break
        instructionsList.append(ChromosomeElem(
            currentCommand, currentValue))
        previousCommand, previousValue = currentCommand, currentValue
        ins_generated += 1
    return instructionsList

def point_storing(current_x, current_y, angle, points):
    x = current_x
    y = current_y
    distancing = 0.1
    steps = 0
    change_axis = 1
    if angle == 0:
        while steps < change_axis:
            abscissa = points.get(x)
            if not abscissa:
                points[x] = []
                abscissa = points.get(x)
                abscissa.append(y)
            else:
                abscissa.append(y)
            y += distancing
            steps += distancing
    else:
        while steps < change_axis:
            cos_rad = math.radians(abs(90 - angle))
            sin_rad = math.radians(90 - angle)
            if steps > 0:
                x += math.cos(cos_rad)*distancing
                y += math.sin(sin_rad)*distancing
            abscissa = points.get(x)
            if not abscissa:
                points[x] = []
                abscissa = points.get(x)
                abscissa.append(y)
            else:
                abscissa.append(y)
            steps += distancing
    return x, y



