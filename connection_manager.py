
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

@tool(examples=["I would like to connect to the ROS server"])
def check_connection(tool_input, cat):
    "Check the connection to the ROS server"
    ros_client, host, port = initialize_connection(cat)
    ros_client.run()
    connection_status = ros_client.is_connected
    if connection_status:
        response = f"Connected to ROS server at {host}:{port}"
        log.info(response)
    else:
        response = f"Not connected to ROS server at {host}:{port}.\nPlease check your settings or verfiy the connection."
        log.warning(response)
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

    