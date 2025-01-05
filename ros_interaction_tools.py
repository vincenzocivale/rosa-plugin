# from cat.mad_hatter.decorators import tool
# from cat.log import log
# import roslibpy
# import connection_manager as cm



# class ROSTopic(BaseModel): #
#     topic_name: str
#     topic_type: str


# @form
# class TopicSubscriptionForm(CatForm): #

#     description = "Form to subscribe to ros topic" 
#     model_class = ROSTopic 
#     start_examples = [ #
#         "Submit to a ROS topic"
#     ]
#     stop_examples = [ #
#         "stop pizza order",
#         "not hungry anymore",
#     ]
#     ask_confirm = True #

#     def submit(self, form_data): #
#         ros_client, host, port = cm.initialize_connection(cat)
#         ros_client.run()
#         topic = roslibpy.Topic(ros_client, topic_name, topic_type)

#         return {
#             "output": f"Pizza order on its way: {form_data}. Estimated time: {time}"
#         }


