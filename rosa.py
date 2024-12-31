from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date
import roslibpy

# System parametres
host_ip = "localhost"
port = 9090

ros_client = roslibpy.Ros(host=host_ip, port=port)

class ROSVersion(Enum):
    a: str = 'ROS1'
    b: str = 'ROS2'

class PluginSettings(BaseModel):
    host_ip: str
    port: int = 9090
    ros_version: ROSVersion = ROSVersion.a


@plugin
def settings_model():
    return PluginSettings

@hook 
def agent_prompt_prefix(prefix, cat):
    prefix = """Your are ROSA (Robot Operating System Agent), an AI agent that can use ROS tools to answer questions 
        about robotics systems. You have a subset of the ROS tools available to you, and you can use them to 
        interact with the robotic system you are integrated with. Your responses should be grounded in real-time 
        information whenever possible using the tools available to you."""
    return prefix


@tool(examples=["I would like to connect to a ROS server"])
def inizialize_ros_client(cat):
    "Inizialize the ROS client to control the robot"
    global ros_client
    ros_client.run()
    return "Connected to ROS server"

@tool(examples=["I would like to disconnect from the ROS server"])
def disconnect_ros_client(cat):
    "Disconnect the ROS client from the robot"
    global ros_client
    ros_client.terminate()
    return "Disconnected from ROS server"

@tool(examples=["I would like to get the list of topics"])
def get_topics(cat):
    "Get the list of topics available in the ROS server"
    global ros_client
    topics = ros_client.get_topics()
    topics_string = "\n".join(topics)
    response = f"The topics available in the ROS server are: \n{topics_string}"

# @tool(examples=["I would like to verfiy the connection to the ROS server"])
# def verify_connection(cat):
#     "Verify the connection to the ROS server"
#     global ros_client
#     connection_status = ros_client.is_connected

#     if connection_status:
#         response = "The connection to the ROS server is successful!"
#     else:
#         response = "Failed to connect to the ROS server. Please check your settings."

#     # Use the cat instance to send the response
#     cat.send_message(response)