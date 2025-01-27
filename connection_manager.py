
from cat.mad_hatter.decorators import tool
from cat.log import log
import roslibpy
import ast
import json
import time

def string_to_dict(dict_string):
    """
    Convert a dictionary string to a Python dictionary

    dict_string: str, the dictionary in string format

    Returns: dict, the dictionary in Python format
    """
    try:
        return ast.literal_eval(dict_string)
    except (ValueError, SyntaxError) as e:
        log.error(f"Failed to convert string to dictionary: {e}")
        return {}

def initialize_connection(cat):
    "Initialize the connection to the ROS server"
    settings = cat.mad_hatter.get_plugin().load_settings()
    host = settings["host_ip"]
    port = settings["port"]

    cat.send_ws_message(content = f"Trying to connect to ROS server at {host}:{port}", msg_type = "chat")
    

    ros_client = roslibpy.Ros(host=host, port=port)

    ros_client.run()

    if ros_client.is_connected:
        cat.send_ws_message(content = f"Connection to ROS server established successfully.", msg_type = "chat")
        return ros_client, host, port
    else:
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

#@tool(examples=["I want to subscribe to a topic in ROS. "])
def subscribe_to_topic(subscription_info: dict, cat):
    """
    Subscribe to a topic in the ROS server. The function must be executed when there's ONLY ONE OPERATION IN PROMPT
    
    subscription_info is input is a dict with keys: topic_name, message_type
    """

    # è necessario convertire subscription_info in un dizionario in quanto stringa
    subscription_info = json.loads(subscription_info)

    cat.send_ws_message(f"tool input {subscription_info}", msg_type = "chat")
    cat.send_ws_message(f"tool input keys {subscription_info.keys()}", msg_type = "chat")
    ros_client, host, port = initialize_connection(cat)

    # Variabile per memorizzare il primo messaggio ricevuto
    first_message = None

    # Flag per indicare se il messaggio è stato ricevuto
    message_received = False

    # Funzione di callback per gestire i messaggi ricevuti
    def callback(message):
        nonlocal first_message, message_received
        if not message_received:
            first_message = message
            message_received = True
            cat.send_ws_message(f"Received message: {message}", msg_type="chat")
            topic.unsubscribe()  # Interrompi la sottoscrizione dopo il primo messaggio
            ros_client.terminate()  # Chiudi la connessione ROS

    # Crea un sottoscrittore (subscriber)
    topic = roslibpy.Topic(ros_client, subscription_info["topic_name"], subscription_info["message_type"])
    topic.subscribe(callback)

    # Attendi il primo messaggio
    while not message_received:
        pass

    return first_message

#@tool(examples=["I want to publish to topic /turtle1/cmd_vel of type geometry_msgs/msg/Twist with linear x=1.0 and angular z=0.5"]) 
def publish_to_topic(publication_info: dict, cat):
    """
        The function must be executed when there's ONLY ONE OPERATION IN PROMPT
        Publish to a topic in the ROS server
        
        publication_info is input is a dict with keys: topic_name, duration (duration of pubblication in seconds), message_type, 
        message_data (Python dictionary representing the content of the ROS message to be published on a topic. 
        It must be structured to comply with the format of the message type specified for the topic)
        """
    
    cat.send_ws_message(f"tool input {publication_info}", msg_type = "chat")

    # è necessario convertire subscription_info in un dizionario in quanto stringa
    #publication_info = json.loads(publication_info)

    ros_client, host, port = initialize_connection(cat)

    # Crea un editore (publisher)
    publisher = roslibpy.Topic(ros_client, publication_info["topic_name"], publication_info["message_type"])

    duration = publication_info.get("duration", 1.0)
    start_time = time.time()
    while (time.time() - start_time) < duration:
        publisher.publish(roslibpy.Message(publication_info["message_data"]))
        time.sleep(0.1)  # 10Hz

    return "Message published successfully. Proceed with the next task or conclude the operation."

@tool()
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
                "duration": float  # The duration of the task in seconds. For tasks that are not time-bound, this value can be None.
            },
            "task_name_2": {  # The unique name of the task 2(string)
                ....
            },
            ...
        }
    """

    cat.send_ws_message(f"tool input {tasks}", msg_type = "chat")
    cat.send_ws_message(f"tool type {type(tasks)}", msg_type = "chat")
    # cat.send_ws_message(f"tool input {tasks["task"]}", msg_type = "chat")
    #cat.send_ws_message(f"tool type {type(tasks['tasks'][0])}", msg_type="chat")

    tasks = json.loads(tasks)

    task_sequence = tasks['tasks'] 
    for task_name in task_sequence.keys():
        task_data = task_sequence[task_name] 
        task_type = task_data["task_type"]
        if task_type == "publish":
            publish_to_topic(task_data, cat)
        elif task_type == "subscribe":
            subscribe_to_topic(task_data, cat)

