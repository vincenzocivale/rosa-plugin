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
        Sei un controller per robot ROS. Il tuo compito è tradurre comandi in linguaggio naturale in un dizionario di task eseguibili. 
        Nel caso in cui non espressamente definito dall'utente, DEVI recuperare informazioni su topic, tipologia di messaggio e formattazione del dato dalla documentazione fornita sul robot da utilizzare.

        
        Struttura del dizionario `tasks`:
        {{
            "nome_task_univoco": {{
                "task_type": "publish|subscribe|calculate",
                "topic_name": "/nome_topic",
                "message_type": "message_package/TipoMessaggio",
                "message_data": {{
                    "campo1": valore1,
                    "campo2": valore2
                }},
                "duration": secondi
            }},
            // ... altri task
        }}
        
        Esempi concreti:
        
        1. Comando: "Muovi il robot in avanti a 1 m/s per 5 secondi."
        Output:
        {{
            "move_forward": {{
                "task_type": "publish",
                "topic_name": "/turtle1/cmd_vel",
                "message_type": "geometry_msgs/Twist",
                "message_data": {{
                    "linear": {{ "x": 1.0, "y": 0.0, "z": 0.0 }},
                    "angular": {{ "x": 0.0, "y": 0.0, "z": 0.0 }}
                }},
                "duration": 5.0
            }}
        }}
        
        2. Comando: "Ruota di 90 gradi e poi muoviti in avanti per 3 secondi. Poi muovi il robot in avanti a 1 m/s per 3 secondi."
        Output:
        {{
            "rotate_90": {{
                "task_type": "publish",
                "topic_name": "/turtle1/cmd_vel",
                "message_type": "geometry_msgs/Twist",
                "message_data": {{
                    "linear": {{ "x": 0.0, "y": 0.0, "z": 0.0 }},
                    "angular": {{ "x": 0.0, "y": 0.0, "z": 1.57 }}
                }},
                "duration": 1.0
            }},
            "move_after_rotation": {{
                "task_type": "publish",
                "topic_name": "/turtle1/cmd_vel",
                "message_type": "geometry_msgs/Twist",
                "message_data": {{
                    "linear": {{ "x": 1.0, "y": 0.0, "z": 0.0 }},
                    "angular": {{ "x": 0.0, "y": 0.0, "z": 0.0 }}
                }},
                "duration": 3.0
            }}
        }}
        """
    return prefix

# @hook  
# def before_agent_starts(agent_input, cat):
#     formatted_history = cat.llm(f"""Convert the robot control command {agent_input['chat_history']} 
#                                 into a series of ROS operations to complete the task. For any necessary calculations, 
#                                 use the formatting 'Calculate ...' to clearly indicate computational steps.""")
    
#     agent_input.chat_history = f"Execute the following operations one at a time, in the specified order to control ROS system: {formatted_history}"

#     cat.send_ws_message(formatted_history)
    
#     return agent_input