import roslibpy

# Topic name and type
topic_name, topic_type = "/client_count", "std_msgs/Int32"

# Create a ROS client
ros_client = roslibpy.Ros(host="172.17.0.1", port=9090)

# Function to handle incoming messages
def message_callback(message):
    print(f"Received message: {message['data']}")

# Run the client and subscribe to the topic
try:
    ros_client.run()  # Establish the connection to ROS
    print("ROS client connected.")

    # Create the topic object
    topic = roslibpy.Topic(ros_client, topic_name, topic_type)
    
    # Subscribe to the topic and set up the callback function
    topic.subscribe(message_callback)
    
    # Keep the program running to receive messages
    print(f"Subscribed to topic {topic_name}. Waiting for messages...")
    input("Press Enter to stop the subscriber...\n")  # Keep the process alive to receive messages
    
    # After the user presses Enter, unsubscribe and close the client
    topic.unsubscribe()
    ros_client.close()
    print("ROS client closed.")
    
except Exception as e:
    print(f"Failed to subscribe to topic {topic_name}: {e}")

       
       
