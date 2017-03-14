import zmq
import time
import pickle
import logging

import data_model

logging.basicConfig(format='%(asctime)-15s - %(name)s - %(message)s')
logger = logging.getLogger('publisher')
logger.setLevel(logging.INFO)

context = zmq.Context()

logger.info('Setting up measurements socket')
measurements_socket = context.socket(zmq.PUB)
measurements_socket.bind('tcp://*:5556')

logger.info('Setting up controller socket')
controller_socket = context.socket(zmq.SUB)
controller_socket.connect("tcp://127.0.0.1:5557")
controller_socket.setsockopt_string(zmq.SUBSCRIBE, '')

# Number of measurement samples to communicate
n = 5

tsm = data_model.ThrusterSystemMeasurements(3)
# Fill in some data
tsm.thrusters[0].direction = 10.0
tsm.thrusters[0].rpm = 14.0
tsm.thrusters[1].direction = 90.0
tsm.thrusters[1].rpm = 84.0
tsm.thrusters[2].direction = -80.0
tsm.thrusters[2].rpm = 30.0

time.sleep(1)

for i in range(n):
    logger.info('Sending thruster measurements {}'.format(repr(tsm)))
    measurements_socket.send(pickle.dumps(tsm))

    logger.info('Waiting for control signal')
    p = controller_socket.recv()
    tsc = pickle.loads(p)
    logger.info('Got demand: {}'.format(repr(tsc)))

    # Set measurements to same values as control system demands
    for thruster_measurement, thruster_control_signal in zip(tsm.thrusters, tsc.thrusters):
        thruster_measurement.direction = thruster_control_signal.demanded_direction
        thruster_measurement.rpm = thruster_control_signal.demanded_rpm

