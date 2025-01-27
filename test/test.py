# import time
# import roslibpy

# def publish_velocity(client, topic_name, linear_x, linear_y, linear_z, angular_x, angular_y, angular_z, duration):
#     """
#     Pubblica messaggi di velocità su un topic per una durata specificata.
#     """
#     publisher = roslibpy.Topic(client, topic_name, 'geometry_msgs/Twist')
#     twist_message = {
#         'linear': {'x': linear_x, 'y': linear_y, 'z': linear_z},
#         'angular': {'x': angular_x, 'y': angular_y, 'z': angular_z}
#     }
    
#     publisher.advertise()
#     start_time = time.time()
#     while time.time() - start_time < duration:
#         publisher.publish(roslibpy.Message(twist_message))
#         time.sleep(0.1)  # Pubblica ogni 100ms
    
#     publisher.unadvertise()

# def main():
#     # Connessione al ROS Master
#     client = roslibpy.Ros(host='localhost', port=9090)
#     client.run()
    
#     try:
#         # Disegna un cerchio
#         print("Disegnando un cerchio...")
#         publish_velocity(client, '/turtle1/cmd_vel', 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 6)

#         # Muoviti in avanti
#         print("Muovendosi in avanti...")
#         publish_velocity(client, '/turtle1/cmd_vel', 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3)

#         # Ruota di 90 gradi
#         print("Ruotando di 90 gradi...")
#         publish_velocity(client, '/turtle1/cmd_vel', 0.0, 0.0, 0.0, 0.0, 0.0, 1.57, 1)

#         print("Operazioni completate.")
#     except Exception as e:
#         print(f"Errore: {e}")
#     finally:
#         client.terminate()

# if __name__ == '__main__':
#     main()
