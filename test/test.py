# import roslibpy

# # Topic name and type
# topic_name, topic_type = "/turtle1/pose", "turtlesim_msgs/msg/Pose"

# # Create a ROS client
# ros_client = roslibpy.Ros(host="172.17.0.1", port=9090)

# # Function to handle incoming messages
# def message_callback(message):
#     print(message.keys())

# # Run the client and subscribe to the topic
# try:
#     ros_client.run()  # Establish the connection to ROS
#     print("ROS client connected.")

#     # Create the topic object
#     topic = roslibpy.Topic(ros_client, topic_name, topic_type)
    
#     # Subscribe to the topic and set up the callback function
#     topic.subscribe(message_callback)
    
#     # Keep the program running to receive messages
#     print(f"Subscribed to topic {topic_name}. Waiting for messages...")
#     input("Press Enter to stop the subscriber...\n")  # Keep the process alive to receive messages
    
#     # After the user presses Enter, unsubscribe and close the client
#     topic.unsubscribe()
#     ros_client.close()
#     print("ROS client closed.")
    
# except Exception as e:
#     print(f"Failed to subscribe to topic {topic_name}: {e}")

       
       
# import roslibpy
# import time

# # Connessione al rosbridge WebSocket
# client = roslibpy.Ros(host='172.18.173.231', port=9090)
# client.run()

# try:
#     # Verifica connessione
#     if client.is_connected:
#         print("Connesso a ROS!")
#     else:
#         raise ConnectionError("Connessione ROS fallita")

#     # Creazione publisher per il comando di movimento
#     publisher = roslibpy.Topic(
#         client,
#         '/turtle1/cmd_vel',  # Topic per controllare il movimento
#         'geometry_msgs/Twist',  # Tipo messaggio per comandi di velocità
#         queue_size=10
#     )

#     # Pubblica il messaggio di movimento (avanti e rotazione)
#     move_cmd = {
#         'linear': {'x': 1.0, 'y': 0.0, 'z': 0.0},  # Velocità lineare in avanti
#         'angular': {'x': 0.0, 'y': 0.0, 'z': 1.0}  # Velocità angolare (rotazione sinistra)
#     }

#     publisher.advertise()  # Registra il publisher

#     print("Inizio pubblicazione comandi...")
#     while client.is_connected:
#         publisher.publish(roslibpy.Message(move_cmd))
#         time.sleep(0.1)  # Riduce il carico sulla CPU

# except KeyboardInterrupt:
#     print("\nInterruzione da tastiera")
# finally:
#     # Pulizia delle risorse
#     if 'publisher' in locals():
#         publisher.unadvertise()
#     client.terminate()
#     print("Connessione chiusa")

# import json 
# input = """{"tasks": {"draw_circle": {"task_type": "publish", "topic_name": "/turtle1/cmd_vel", "message_type": "geometry_msgs/msg/Twist", "message_data": {"linear": {"x": 1.0, "y": 0.0, "z": 0.0}, "angular": {"x": 0.0, "y": 0.0, "z": 1.0}}, "duration": 6}, "move_forward": {"task_type": "publish", "topic_name": "/turtle1/cmd_vel", "message_type": "geometry_msgs/msg/Twist", "message_data": {"linear": {"x": 1.0, "y": 0.0, "z": 0.0}, "angular": {"x": 0.0, "y": 0.0, "z": 0.0}}, "duration": 3}, "turn_right": {"task_type": "publish", "topic_name": "/turtle1/cmd_vel", "message_type": "geometry_msgs/msg/Twist", "message_data": {"linear": {"x": 0.0, "y": 0.0, "z": 0.0}, "angular": {"x": 0.0, "y": 0.0, "z": -1.57}}, "duration": 1}}}"""
# tasks = json.loads(input)
# task_sequence = tasks['tasks'] 
# for task_name in task_sequence.keys():
#     task_data = task_sequence[task_name]
#     task_type = task_data["task_type"]
#     print(f"Executing task {task_name} of type {task_type}...")
        