import roslibpy
import time
from typing import Tuple, List

def initialize_ros_client(host_ip: str = "localhost", port: int = 9090, timeout: int = 10) -> Tuple[bool, str, roslibpy.Ros]:
    """
    Initialize the ROS client and verify the connection status.
    
    Args:
        host_ip (str): The IP address of the ROS server
        port (int): The port number for the connection
        timeout (int): Maximum time to wait for connection in seconds
    
    Returns:
        Tuple[bool, str, roslibpy.Ros]: (connection_success, status_message, ros_client)
    """
    try:
        # Initialize ROS client
        ros_client = roslibpy.Ros(host=host_ip, port=port)
        
        # Start the client
        ros_client.run()
        
        # Wait for connection with timeout
        start_time = time.time()
        while not ros_client.is_connected:
            if time.time() - start_time > timeout:
                ros_client.close()
                return False, f"Connection timeout after {timeout} seconds", None
            time.sleep(0.1)
        
        if ros_client.is_connected:
            return True, f"Successfully connected to ROS server at {host_ip}:{port}", ros_client
        else:
            return False, "Failed to establish connection", None
            
    except Exception as e:
        return False, f"Connection error: {str(e)}", None

def get_topics(ros_client: roslibpy.Ros) -> Tuple[bool, str, List[str]]:
    """
    Get the list of topics available in the ROS server.
    
    Args:
        ros_client: The connected ROS client
        
    Returns:
        Tuple[bool, str, List[str]]: (success, message, topics_list)
    """
    try:
        if not ros_client or not ros_client.is_connected:
            return False, "ROS client not connected", []
            
        topics = ros_client.get_topics()
        if not topics:
            return False, "No topics found", []
            
        return True, "Topics retrieved successfully", topics
        
    except Exception as e:
        return False, f"Error getting topics: {str(e)}", []

def main():
    # Configuration
    HOST_IP = "localhost"
    PORT = 9090
    TIMEOUT = 10
    
    # Try to connect
    success, message, ros_client = initialize_ros_client(HOST_IP, PORT, TIMEOUT)
    
    # Print connection result
    if success:
        print(f"\n✅ {message}")
        
        # Get and print topics
        topics_success, topics_message, topics = get_topics(ros_client)
        if topics_success:
            print("\n📋 Topics disponibili nel server ROS:")
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic}")
        else:
            print(f"\n❌ {topics_message}")
    else:
        print(f"\n❌ {message}")
        print("\nPossibili soluzioni:")
        print("1. Verifica che il server ROS bridge sia in esecuzione")
        print("2. Controlla che la porta 9090 sia disponibile")
        print("3. Assicurati che l'indirizzo IP sia corretto")
        print("4. Verifica che non ci siano firewall che bloccano la connessione")
    
    # Cleanup
    if ros_client and ros_client.is_connected:
        ros_client.close()

if __name__ == "__main__":
    main()