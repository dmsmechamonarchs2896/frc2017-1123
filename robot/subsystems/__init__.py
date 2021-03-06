"""
All subsystems should be imported here and instantiated inside the init method.
If you want your subsystem to be accessible to commands, you must add a variable
for it in the global scope.
"""

from wpilib.robotbase import RobotBase

from .climbingmech import ClimbingMech
from .gearmech import GearMech
from .motors import Motors
from .dumper import Dumper

motors = None
gear_mech = None
climbing_mech = None
dumper = None


def init():
    """
    Creates all subsystems. You must run this before any commands are
    instantiated. Do not run it more than once.
    """
    global motors, gear_mech, climbing_mech, dumper

    '''
    Some tests call startCompetition multiple times, so don't throw an error if
    called more than once in that case.
    '''
    if motors is not None and not RobotBase.isSimulation():  # pragma: no cover
        raise RuntimeError('Subsystems have already been initialized')

    motors = Motors()

    gear_mech = GearMech()

    climbing_mech = ClimbingMech()

    dumper = Dumper()
