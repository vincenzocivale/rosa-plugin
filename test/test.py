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


# import time
# import roslibpy

# def publish_pose_and_move():
#     # Connessione al ROS master
#     ros = roslibpy.Ros(host='localhost', port=9090)
#     ros.run()

#     if ros.is_connected:
#         print('Connesso a ROS master.')

#         # Publisher sul topic /turtle1/pose (modificato per adattarsi alla logica del movimento)
#         pose_publisher = roslibpy.Topic(ros, '/turtle1/pose', 'turtlesim_msgs/msg/Pose')

#         # Messaggio da pubblicare per la posa iniziale
#         initial_message = {
#             'x': 5.0,
#             'y': 2.5,
#             'theta': 0.05,  # Angolo iniziale
#             'linear_velocity': 0.0,
#             'angular_velocity': 0.0
#         }

#         # Pubblicazione della posa iniziale per 3 secondi
#         start_time = time.time()
#         while time.time() - start_time < 3.0:
#             pose_publisher.publish(roslibpy.Message(initial_message))
#             print(f'Messaggio pubblicato: {initial_message}')
#             time.sleep(0.1)  # Intervallo di pubblicazione (10 Hz)

#         # Publisher per il movimento in avanti (cmd_vel)
#         cmd_vel_publisher = roslibpy.Topic(ros, '/turtle1/cmd_vel', 'geometry_msgs/Twist')

#         # Messaggio per muovere la tartaruga in avanti (velocità lineare positiva, velocità angolare nulla)
#         move_message = {
#             'linear': {'x': 1.0, 'y': 0.0, 'z': 0.0},  # Velocità lineare in avanti
#             'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}  # Nessuna rotazione
#         }

#         # Pubblicazione per 5 secondi per muovere la tartaruga in avanti
#         start_time = time.time()
#         while time.time() - start_time < 5.0:
#             cmd_vel_publisher.publish(roslibpy.Message(move_message))
#             print(f'Movimento in avanti: {move_message}')
#             time.sleep(0.1)  # Intervallo di pubblicazione (10 Hz)

#         # Ferma la tartaruga (opzionale)
#         stop_message = {
#             'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},  # Ferma la tartaruga
#             'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}  # Nessuna rotazione
#         }
#         cmd_vel_publisher.publish(roslibpy.Message(stop_message))
#         print(f'Movimento fermato: {stop_message}')

#         # Chiudi i publisher
#         pose_publisher.unadvertise()
#         cmd_vel_publisher.unadvertise()

#     else:
#         print('Connessione a ROS master fallita.')

#     # Disconnessione da ROS
#     ros.terminate()

# if __name__ == '__main__':
#     publish_pose_and_move()
