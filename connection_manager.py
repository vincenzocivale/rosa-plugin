
from cat.mad_hatter.decorators import tool
from cat.log import log
import roslibpy

def initialize_connection(cat):
    "Initialize the connection to the ROS server"
    settings = cat.mad_hatter.get_plugin().load_settings()
    host = settings["host_ip"]
    port = settings["port"]

    ros_client = roslibpy.Ros(host=host, port=port)
    return ros_client, host, port

@tool(examples=["I would like to connect to the ROS server"], return_direct=True)
def check_connection(tool_input, cat):
    "Check the connection to the ROS server"
    ros_client, host, port = initialize_connection(cat)
    try:
        ros_client.run()
        connection_status = ros_client.is_connected
        if connection_status:
            response = f"Connected to ROS server at {host}:{port}"
            log.info(response)
        else:
            response = (
                            f"Error: Unable to connect to the ROS server at {host}:{port}.\n"
                            "Please verify your settings and ensure the connection is properly established."
                        )
            log.warning(response)
            
    except Exception as e:
        response = f"Failed to connect to ROS server at {host}:{port}.\nError: {str(e)}"
        log.error(response)
    return response

@tool(examples=["I would like to get the list of topics"], return_direct=True)
def get_topics(tool_input, cat):
    "Get the list of topics available in the ROS server"
    ros_client, host, port = initialize_connection(cat)
    ros_client.run()
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

@tool(return_direct=True, example=["I want to subscribe to a topic in ROS. The topic is /client_count and the type is std_msgs/msg/Int32. Please subscribe to it."])
def subscribe_to_topic(tool_input, cat):
    """
    Subscribe to a topic in the ROS server
    
    """
    topic_name, topic_type = "/client_count", "std_msgs/msg/Int32"
    log.warning(f"Topic name: {topic_name} Type{topic_type}")
    ros_client, host, port = cm.initialize_connection(cat)
    ros_client.run()
    try:
        topic = roslibpy.Topic(ros_client, topic_name, topic_type)
        topic.subscribe(lambda message: log.info(f"Received message: {message['data']}"))
    except Exception as e:
        log.error(f"Failed to subscribe to topic {topic_name}: {e}")
        return f"Error: Failed to subscribe to topic {topic_name}."

    # Return confirmation response
    response = f"Subscribed to topic {topic_name}."
    return response
