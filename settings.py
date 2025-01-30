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
        You are a controller for a ROS robot. Your task is to translate commands in natural language into a dictionary of executable tasks.
        In case the user has not explicitly defined something, YOU MUST retrieve information about topics, message types, and data formatting from the documentation provided for the robot to be used.

        Structure of the tasks dictionary:

        {
            "unique_task_name": {
                "task_type": "publish|subscribe|calculate",
                "topic_name": "/topic_name",
                "message_type": "message_package/MessageType",
                "message_data": {
                    "field1": value1,
                    "field2": value2
                },
                "duration": seconds
            },
            // ... other tasks
        }

        Concrete examples:

            Command: "Move the robot forward at 1 m/s for 5 seconds." Output:

        {
            "move_forward": {
                "task_type": "publish",
                "topic_name": "/turtle1/cmd_vel",
                "message_type": "geometry_msgs/Twist",
                "message_data": {
                    "linear": { "x": 1.0, "y": 0.0, "z": 0.0 },
                    "angular": { "x": 0.0, "y": 0.0, "z": 0.0 }
                },
                "duration": 5.0
            }
        }

            Command: "Rotate by 90 degrees and then move forward for 3 seconds. Then move the robot forward at 1 m/s for 3 seconds." Output:

        {
            "rotate_90": {
                "task_type": "publish",
                "topic_name": "/turtle1/cmd_vel",
                "message_type": "geometry_msgs/Twist",
                "message_data": {
                    "linear": { "x": 0.0, "y": 0.0, "z": 0.0 },
                    "angular": { "x": 0.0, "y": 0.0, "z": 1.57 }
                },
                "duration": 1.0
            },
            "move_after_rotation": {
                "task_type": "publish",
                "topic_name": "/turtle1/cmd_vel",
                "message_type": "geometry_msgs/Twist",
                "message_data": {
                    "linear": { "x": 1.0, "y": 0.0, "z": 0.0 },
                    "angular": { "x": 0.0, "y": 0.0, "z": 0.0 }
                },
                "duration": 3.0
            }
        }
        """
    return prefix

