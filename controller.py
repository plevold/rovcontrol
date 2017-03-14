import zmq
import pickle
import logging

import data_model

logging.basicConfig(format='%(asctime)-15s - %(name)s - %(message)s')
logger = logging.getLogger('controller')
logger.setLevel(logging.INFO)

#  Socket to talk to server
context = zmq.Context()

logger.info('Setting up measurements socket')
measurements_socket = context.socket(zmq.SUB)
measurements_socket.connect("tcp://127.0.0.1:5556")
measurements_socket.setsockopt_string(zmq.SUBSCRIBE, '')

logger.info('Setting up controller socket')
controller_socket = context.socket(zmq.PUB)
controller_socket.bind('tcp://*:5557')

tscs = data_model.ThrusterSystemControlSignals(3)

while True:
    logger.info('Waiting for measurements...')
    p = measurements_socket.recv()
    tsm = pickle.loads(p)
    logger.info('Received: {}'.format(repr(tsm)))

    # Increase demand slightly compared to measurements
    for thruster_measurement, thruster_control_signal in zip(tsm.thrusters, tscs.thrusters):
        thruster_control_signal.demanded_direction = thruster_measurement.direction + 1.0
        thruster_control_signal.demanded_rpm = thruster_measurement.rpm + 1.0
    
    logger.info('Sending demand: {}'.format(repr(tscs)))
    controller_socket.send(pickle.dumps(tscs))

