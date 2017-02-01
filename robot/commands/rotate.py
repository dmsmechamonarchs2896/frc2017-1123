from robotpy_ext.common_drivers.navx import AHRS
from wpilib.command import PIDCommand

import subsystems


class Rotate(PIDCommand):
    """
    This command uses the NavX to rotate to the specified angle.
    """

    def __init__(self, angle):
        # PID constants
        kp = 0.005
        ki = 0.0
        kd = 0.0
        kf = 0.0
        ktolerance = 2.0  # tolerance of 2 degrees

        super().__init__(kp, ki, kd, 0.05, kf, "Rotate to angle {}".format(angle))

        self.requires(subsystems.motors)

        self.ahrs = AHRS.create_spi()
        self.rate = 1.0

        turnController = self.getPIDController()
        turnController.setInputRange(-180.0, 180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(ktolerance)
        turnController.setContinuous(True)

        # self.rotateToAngleRate = 0.0
        turnController.setSetpoint(angle)

        # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        # wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", self.turnController)

    def returnPIDInput(self):
        return self.ahrs.getYaw()

    def usePIDOutput(self, output):
        self.rate = output
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(-output, output)

    def isFinished(self):
        return abs(self.rate) < 0.01
