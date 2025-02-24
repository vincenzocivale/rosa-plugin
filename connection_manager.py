
from cat.mad_hatter.decorators import tool
from cat.log import log
import roslibpy
import json
import time

def initialize_connection(cat):
    "Initialize the connection to the ROS server"
    settings = cat.mad_hatter.get_plugin().load_settings()
    host = settings["host_ip"]
    port = settings["port"]

    cat.send_ws_message(content = f"Trying to connect to ROS server at {host}:{port}", msg_type = "chat")
    
    try:
        ros_client = roslibpy.Ros(host=host, port=port)

        ros_client.run()
        cat.send_ws_message(content = f"Connection to ROS server established successfully.", msg_type = "chat")
        return ros_client, host, port
    
    except:
        cat.send_ws_message(content = f"Failed to connect to ROS server at {host}:{port}", msg_type = "chat")
        


@tool(examples=["I would like to get the list of topics"], return_direct=True)
def get_topics(tool_input, cat):
    "Get the list of topics available in the ROS server"
    ros_client, host, port = initialize_connection(cat)
    topics = ros_client.get_topics()
    topics_string = "\n".join(topics)
    response = f"The topics available in the ROS server are: \n{topics_string}"
    return response

@tool(examples=["I would like to change the ROS server IP"], return_direct=True)
def change_ros_server_ip(tool_input, cat):
    """
    Change the IP address of the ROS server in the settings
    
    tool_input reppresents the new IP address set by the user

    """
    new_ip = tool_input
    
    settings = cat.mad_hatter.get_plugin().load_settings()
    settings["host_ip"] = new_ip
    cat.mad_hatter.get_plugin().save_settings(settings)
    response = f"ROS server IP address has been changed to {new_ip}."
    log.info(response)
    return response


def subscribe_to_topic(sub_info: dict, ros_client, cat):
    """
    Subscribe to a topic in the ROS server and stop after receiving the first message.
    
    :param sub_info: Dictionary containing 'topic_name' and 'message_type'
    :param ros_client: The ROS client (roslibpy.Ros)
    :param cat: (Optional) An object to send log or chat messages
    """
    listener = roslibpy.Topic(ros_client, sub_info['topic_name'], sub_info['message_type'])

    # Callback function that is called when a message is received
    def message_callback(message):
        cat.send_ws_message(f"Received message: {message}", msg_type = "chat")
        
        # After receiving the first message, unsubscribe
        listener.unsubscribe()
    
    # Subscribe to the topic with the callback function
    listener.subscribe(message_callback)

    

def publish_to_topic(publication_info: dict, ros_client, cat):
    """
        The function must be executed when there's ONLY ONE OPERATION IN PROMPT
        Publish to a topic in the ROS server
        
        publication_info is input is a dict with keys: topic_name, duration (duration of pubblication in seconds), message_type, 
        message_data (Python dictionary representing the content of the ROS message to be published on a topic. 
        It must be structured to comply with the format of the message type specified for the topic)
        """
    
    cat.send_ws_message(f"Pubblishing to topic {publication_info['topic_name']}", msg_type = "chat")

    publisher = roslibpy.Topic(ros_client, publication_info["topic_name"], publication_info["message_type"])

    duration = publication_info.get("duration", 1.0)
    start_time = time.time()
    while (time.time() - start_time) < duration:
        publisher.publish(roslibpy.Message(publication_info["message_data"]))
        time.sleep(0.1)  # 10Hz

    return "Message published successfully. Proceed with the next task or conclude the operation."

@tool(return_direct=True, examples=["I would like to publish to the ROS topic /turtle1/cmd_vel of type geometry_msgs/Twist. The publication should be performed for 5 seconds with ...", "I would like to subscribe to the ROS topic /turtle1/cmd_vel"])
def sequence_task_execution(tasks: dict, cat):
    """
        The `tasks` dictionary defines a set of operations (tasks) to be executed in a ROS-based robot control system. Each key in the dictionary represents a unique task, and the value is a dictionary containing all necessary details to execute that task.

        Structure of the `tasks` dictionary:
        {
            "task_name": {  # The unique name of the task (string)
                "task_type": string,  # The type of the task (string). Possible values: "publish", "subscribe", "calculate", etc.
                "topic_name": string "/topic_name",  # The ROS topic associated with the task.
                "message_type": string "message_package/MessageType",  # The ROS message type for the task (string), e.g., "geometry_msgs/Twist".
                "message_data": dict "Python dictionary representing the content of the ROS message to be published on a topic. It must be structured to comply with the format of the message type specified for the topic,
                "duration": float | None # The duration of the task in seconds. For tasks that are not time-bound, this value can be None.
            },
            "task_name_2": {  # The unique name of the task 2(string)
                ....
            },
            ...
        }
    """

    ros_client, host, port = initialize_connection(cat)

    cat.send_ws_message(f"tool input {tasks}")

    tasks = json.loads(tasks)
    if "tasks" in tasks.keys():
        tasks = tasks['tasks'] 
    for task_name in tasks.keys():
        task_data = tasks[task_name] 
        task_type = task_data["task_type"]
        if task_type == "publish":
            publish_to_topic(task_data, ros_client, cat)
        elif task_type == "subscribe":
            subscribe_to_topic(task_data, ros_client, cat)
    
    ros_client.close()

    return "All tasks executed successfully. Proceed with the next task or conclude the operation."

