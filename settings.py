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
    prefix = """
        Sei un controller per robot ROS. Il tuo compito è tradurre comandi in linguaggio naturale in una sequenza di task eseguibili.
    
        I task devono essere in formato JSON, con questa struttura:
        {
            "tasks": [
                {
                    "action": string,  # The type of the task (string). Possible values: "publish", "subscribe", "calculate",
                    "topic_name": string "/topic_name",  # The ROS topic associated with the task
                    "message_type": string "message_package/MessageType",  # The ROS message type for the task (string), e.g., "geometry_msgs/Twist".
                    "message_data": dict "Python dictionary representing the content of the ROS message to be published on a topic. It must be structured to comply with the format of the message type specified for the topic,
                    "duration": float  # The duration of the task in seconds. For tasks that are not time-bound, this value can be None.
                }
            ]
        } 
        
        """
    return prefix

# @hook  
# def before_agent_starts(agent_input, cat):
#     formatted_history = cat.llm(f"""Convert the robot control command {agent_input['chat_history']} 
#                                 into a series of ROS operations to complete the task. For any necessary calculations, 
#                                 use the formatting 'Calculate ...' to clearly indicate computational steps.""")
    
#     agent_input["chat_history"] = f"Execute the following operations one at a time, in the specified order to control ROS system: {formatted_history}"

#     cat.send_ws_message(formatted_history)
    
#     return agent_input