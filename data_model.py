import os

class ThrusterMeasurements:

    def __init__(self):
        self.direction = 0.0
        self.rpm = 0.0


    def __repr__(self):
        return '<ThrusterMeasurements direction={}, rpm={}>'    \
            .format(self.direction, self.rpm)


class ThrusterSystemMeasurements:

    def __init__(self, num_thrusters):
        self.thrusters = [ThrusterMeasurements() for i in range(num_thrusters)]


    def __repr__(self):
        representation = '<ThrusterSystemMeasurements {}'.format(os.linesep)
        for thruster in self.thrusters:
            representation += '    {}{}'.format(repr(thruster), os.linesep)
        representation += '    >'
        return representation


class ThrusterControlSignal:

    def __init__(self):
        self.demanded_direction = 0.0
        self.demanded_rpm = 0.0


    def __repr__(self):
        return '<ThrusterControlSignal direction={}, rpm={}>'    \
            .format(self.demanded_direction, self.demanded_rpm)


class ThrusterSystemControlSignals:

    def __init__(self, num_thrusters):
        self.thrusters = [ThrusterControlSignal() for i in range(num_thrusters)]


    def __repr__(self):
        representation = '<ThrusterSystemControlSignals {}'.format(os.linesep)
        for thruster in self.thrusters:
            representation += '    {}{}'.format(repr(thruster), os.linesep)
        representation += '    >'
        return representation
