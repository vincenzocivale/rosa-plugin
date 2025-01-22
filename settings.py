from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date
import time
import roslibpy


class ROSVersion(Enum):
    a: str = 'ROS1'
    b: str = 'ROS2'

class PluginSettings(BaseModel):
    host_ip: str = "localhost"
    port: int = 9090
    ros_version: ROSVersion = ROSVersion.a
    wolfram_alpha_api_key: str = "None"


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

# @hook  
# def before_agent_starts(agent_input, cat):
#     formatted_history = cat.llm(f"""Convert the robot control command {agent_input['chat_history']} 
#                                 into a series of ROS operations to complete the task. For any necessary calculations, 
#                                 use the formatting 'Calculate ...' to clearly indicate computational steps.""")
    
#     agent_input["chat_history"] = f"Execute the following operations one at a time, in the specified order to control ROS system: {formatted_history}"

#     cat.send_ws_message(formatted_history)
    
#     return agent_input