from cat.mad_hatter.decorators import tool
from cat.log import log
import roslibpy
import connection_manager as cm

@tool
def subscribe_to_topic(tool_input, cat):
    """
    Subscribe to a topic in the ROS server
    
    tool_input represents the topic name to subscribe and the type of the topic, divided by a comma.
    
    """
    topic_name, topic_type = tool_input.split(",")
    ros_client, host, port = cm.initialize_connection(cat)
    ros_client.run()
    topic = roslibpy.Topic(ros_client, topic_name, topic_type)
    topic.subscribe(lambda message: log.info(f"Received message: {message['data']}"))
    response = f"Subscribed to topic {topic_name}."
    return response

