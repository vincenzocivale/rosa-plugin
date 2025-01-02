from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date
import time
import roslibpy

# System parametres
host_ip = "localhost"
port = 9090
timeout = 10

ros_client = roslibpy.Ros(host=host_ip, port=port)

class ROSVersion(Enum):
    a: str = 'ROS1'
    b: str = 'ROS2'

class PluginSettings(BaseModel):
    host_ip: str = "localhost"
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


@tool(examples=["I would like to disconnect from the ROS server"])
def disconnect_ros_client(cat):
    "Disconnect the ROS client from the robot"
    global ros_client
    ros_client.terminate()
    return "Disconnected from ROS server"



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

# @tool(examples=["I would like to connect to a ROS server"])
# def inizialize_ros_client(tool_input, cat):
#     """
#     Tool for establishing a connection with a ROS (Robot Operating System) server.
    
#     This tool should be used when:
#     - An initial connection needs to be established with a robot or robotic system
#     - The user mentions the need to communicate or interact with ROS
#     - There's a request to control or command a robot
#     - References are made to "ROS connection", "ROS server", or "robot control"
#     - A robotic control session needs to be initiated
#     - A communication bridge with a ROS system needs to be established
#     - Keywords like "connect to robot", "start ROS", or "initialize robot connection" are mentioned
    
#     """

#     ros_client = roslibpy.Ros(host="localhost", port=9090)
#     cat.send_ws_message(msg_type='chat', content=f"Connecting to ROS server at localhost:")
#     ros_client.run()
#     start_time = time.time()
#     while not ros_client.is_connected:
#         if time.time() - start_time > timeout:
#             ros_client.close()
#             cat.send_ws_message(msg_type='chat', content=f"Connection timeout after {timeout} seconds")
#             return False 
#         time.sleep(0.1)
#     cat.send_ws_message(msg_type='chat', content=f"Successfully connected to ROS server at {host_ip}:{port}")
#     return True