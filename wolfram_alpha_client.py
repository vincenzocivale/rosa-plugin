# # This module is based on the work of the wolfram-alpha-cat plugin available at:
# # https://github.com/pazoff/wolfram-alpha-cat.git
# #
# # This module implements code to solve mathematical operations using the Wolfram Alpha API.
# # It provides functions to query Wolfram Alpha and parse its responses, enabling the integration
# # of advanced mathematical computation capabilities into the ROSA (Robot Operating System Agent) plugin.
# #
# # The plugin is based on the Full Results API of Wolfram Alpha.
# # A description of the various types of Wolfram Alpha APIs is available at:
# # https://products.wolframalpha.com/api


# from cat.mad_hatter.decorators import tool, hook, plugin
# from cat.log import log
# import wolframalpha

# def parse_wolfram_alpha_response(data):
#     output = ""

#     for pod in data['pod']:
#         title = pod['@title']
#         output += f"<br><b>{title}:</b>\n"

#         if 'subpod' in pod:
#             subpod = pod['subpod']
#             if isinstance(subpod, list):
#                 for sp in subpod:
#                     plaintext = sp['plaintext']
#                     if plaintext:
#                         output += f"{plaintext}<br>\n"
#             else:
#                 plaintext = subpod['plaintext']
#                 if plaintext:
#                     output += f"{plaintext}<br>\n"
#         try:
#             img_src = pod.get('subpod', {}).get('img', {}).get('@src')
#             if img_src:
#                 output += f"<img src='{img_src}' alt='{title}' title='{title}'/>\n"
#         except:
#             pass

#         output += "\n"
#     try:
#         sources = data.get('sources', {}).get('source')
#         if sources:
#             source_text = sources.get('@text', '')
#             source_url = sources.get('@url', '')
#             output += f"<b>Source:</b>\n{source_text} (More information: {source_url})\n"
#     except:
#         pass

#     return output

# @tool(examples=["Calculate with wolfram ..."])
# def query_wolfram_alpha(tool_input, cat):
#     """
#     This tool allows the LLM to perform mathematical operations by querying the Wolfram Alpha API.
#     Use this tool whenever a mathematical operation needs to be solved.

#     Parameters:
#     - tool_input (str): The text of the query describing the mathematical operation to be solved by Wolfram Alpha.
#     """
#     # Load the plugin settings
#     settings = cat.mad_hatter.get_plugin().load_settings()
#     wolfram_alpha_api_key = settings.get("wolfram_alpha_api_key")

#     # Check for a wolfram_alpha_App_ID
#     if (wolfram_alpha_api_key is None) or (wolfram_alpha_api_key == ""):
#         no_app_id = 'Missing Wolfram Alpha App ID in the plugin settings. Get the App ID from: https://products.wolframalpha.com/api'
#         return no_app_id

#     try:
#         # Initialize the Wolfram Alpha client
#         client = wolframalpha.Client(wolfram_alpha_api_key)

#         result_text = ""  # Initialize an empty string to accumulate results

#         res = client.query(tool_input)

#         for pod in res.pods:
#             for sub in pod.subpods:
#                 if sub.plaintext is not None:
#                     result_text += sub.plaintext + " <br><br> "  # Append plaintext result to the string variable

#         if len(result_text) == 0:
#             log.warning("Wolfram Alpha has returned no results - " + str(res))
#             #return "Wolfram Alpha has returned no results."
#             return
#         else:
#             try:
#                 parsed_text = parse_wolfram_alpha_response(res)
#             except Exception as err:
#                 log.error(str(err))
#                 parsed_text = result_text

#             return parsed_text

#     except Exception as e:
#         # Handle any exceptions that occur during the Wolfram Alpha query
#         error_message = f"Wolfram Alpha Cat: An error occurred: {str(e)}"
#         log.error(error_message)
#         return error_message


# Execute the following tasks using ROS:

#     Draw a circle: Publish a message on the topic /turtle1/cmd_vel of type geometry_msgs/Twist with the following data:
#         linear.x = 1.0 (constant linear speed)
#         angular.z = 1.0 (constant angular speed) Keep publishing this message for 6 seconds.
#     Move forward for 3 seconds: Publish a message on the same topic /turtle1/cmd_vel of type geometry_msgs/Twist with the following data:
#         linear.x = 1.0 (constant linear speed)
#         angular.z = 0.0 (no rotation). Keep publishing this message for 3 seconds.
#     Turn 90 degrees: Publish a message on the topic /turtle1/cmd_vel of type geometry_msgs/Twist with the following data:
#         linear.x = 0.0 (no linear speed)
#         angular.z = 1.57 (angular speed for a 90-degree turn). Keep publishing this message for 1 second.