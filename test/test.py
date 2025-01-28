from __future__ import print_function
import roslibpy

client = roslibpy.Ros(host='localhost', port=9090)
client.run()

listener = roslibpy.Topic(client, '/turtle1/pose', 'turtlesim_msgs/msg/Pose')
listener.subscribe(lambda message: print('Heard talking: ' + str(message)))

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()