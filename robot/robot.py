#!/usr/bin/env python3

import logging

import wpilib
from commandbased import CommandBasedRobot
from networktables import NetworkTables

import subsystems
from commands.autonomous import AutonomousProgram
from commands.respondtocontroller import RespondToController
from commands.updatenetworktables import UpdateNetworkTables
from inputs import navx, oi, sonar, switches


class Robot(CommandBasedRobot):
    def robotInit(self):
        """
        Set up everything.
        """

        subsystems.init()

        self.logger = logging.getLogger("robot")
        self.sd = NetworkTables.getTable("SmartDashboard")

        # set autonomous modes
        self.sd.putStringArray("autonomous/options",
                               ["left", "center", "right", "boilerleft", "boilerright", "borkleft", "borkright"])
        self.sd.putString("autonomous/selected", "left")
        self.sd.putBoolean("isautonomous", False)

        # Rotate PID values (for tuning)
        self.sd.putNumber("rotate/kp", 0.007)
        self.sd.putNumber("rotate/ki", 0.001)
        self.sd.putNumber("rotate/kd", 0.05)
        self.sd.putNumber("rotate/kf", 0.0)

        # drive-to-rod PID values (for tuning)
        self.sd.putNumber("rod/kp", 0.15)
        self.sd.putNumber("rod/ki", 0)
        self.sd.putNumber("rod/kd", 0)
        self.sd.putNumber("rod/kf", 0.0)
        self.sd.putNumber("rod/ktolerance", 0)

        # RectifiedDrive PID values (for tuning)
        self.sd.putNumber("drive/kp", 0.07)
        self.sd.putNumber("drive/ki", 0.0)
        self.sd.putNumber("drive/kd", 0)
        self.sd.putNumber("drive/kf", 0.05)
        self.sd.putNumber("drive/ktolerance", 0.1)

        # Motor PID values (for tuning)
        self.sd.putNumber("motors/kp", 0.3)
        self.sd.putNumber("motors/ki", 0)
        self.sd.putNumber("motors/kd", 0)
        self.sd.putNumber("motors/kf", 0.7)

        self.sd.putNumber("direction", 1)

        self.sd.putBoolean("lockonRunning", False)

        self.sd.putBoolean("climbDownCommand", False)

        self.sd.putBoolean("slowmode", False)

        navx.init()
        sonar.init()
        oi.init()
        switches.init()
        wpilib.CameraServer.launch('inputs/camera.py:start')

    def autonomousInit(self):
        self.sd.putBoolean("isautonomous", True)
        UpdateNetworkTables().start()
        if self.sd.containsKey("autonomous/selected"):
            AutonomousProgram(self.sd.getString("autonomous/selected")).start()
        else:
            # if not set for some reason (bad!), just use center mode
            AutonomousProgram("center").start()
        self.logger.info("Started autonomous.")

    def teleopInit(self):
        self.sd.putBoolean("isautonomous", False)
        self.sd.putBoolean("timeRunning", True)  # start dashboard timer
        RespondToController().start()
        UpdateNetworkTables().start()
        self.logger.info("Started teleop.")


if __name__ == '__main__':
    wpilib.run(Robot)
