from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from get_creator_email import get_creator_email
import requests

import os
import sys

import pika
import json
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Enrollment API',
    description='API to enrol users into projects (subgrps). Notifies admin when all users in a group have been enrolled. Performs logging functions.',
)



# URLs for simple microservices 
subgroup_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup" 
# user_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/UserAPI_REST/rest/v1/user" 
group_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/GroupAPI_REST/rest/v1/group"
# log_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/LogAPI_REST/rest/v1/"
# notification_microservice_base_url = ""

load_dotenv()
# load notif.env file
rabbitmq_host_notif = os.getenv('HOSTNAME')
rabbitmq_port_notif = os.getenv('PORT')
rabbitmq_exchange_notif = os.getenv('EXCHANGE_NAME')
rabbitmq_exchange_type_notif = os.getenv('EXCHANGE_TYPE') 
rabbitmq_queue_notif = os.getenv('QUEUE_NAME_2')
rabbitmq_routing_key_notif = os.getenv('ROUTING_KEY_2')  

# load log.env file
rabbitmq_host_log = os.getenv('HOSTNAME')
rabbitmq_port_log = os.getenv('PORT')
rabbitmq_exchange_log = os.getenv('EXCHANGE_NAME')
rabbitmq_exchange_type_log = os.getenv('EXCHANGE_TYPE') 
rabbitmq_queue_log = os.getenv('QUEUE_NAME_1')
rabbitmq_routing_key_log = os.getenv('ROUTING_KEY_1') 


# Define your models
user_group_model = api.model('UserGroup', {
    'userId': fields.String(required=True, description='User ID'),
    'groupId': fields.String(required=True, description='Group ID'),
})

# Replace @app.route with @api.route and define your endpoint as a Resource
@api.route('/enrollment')
class Enrollment(Resource):
    @api.doc('get_subgroups_of_group')
    @api.expect(user_group_model)
    def get(self):
        if request.is_json:
            try:    
                user_id = request.json.get('userId')
                group_id = request.json.get('groupId')

                # 1. Call [GET] get user's groups API from group microservice to get user groups
                user_groups_response = requests.get(f'{group_microservice_base_url}/usergroup/{user_id}', headers={"X-Group-AppId": os.getenv("X_Group_AppId"), "X-Group-Key": os.getenv("X_Group_Key")})
                user_groups = user_groups_response.json()["UserGroup"]["groups"]

                # 2. For each group user is in, call [GET] get group's subgroup API from subgroup microservice to get subgroups of the group
                subgroups = []
                for group in user_groups:
                    group_id = group['groupId']
                    subgroup_response = requests.get(f'{subgroup_microservice_base_url}/groupsubgroup/{group_id}', headers={"X-SubGroup-AppId": os.getenv("X_SubGroup_AppId"), "X-SubGroup-Key": os.getenv("X_SubGroup_Key")})
                    subgroups_of_group = subgroup_response.json()["GroupSubGroup"]["subGroups"]
                    subgroups.extend(subgroups_of_group)

                # 3. Consolidate list of groups and subgroups and return to UI
                consolidated_data = {
                    'userGroups': user_groups,
                    'subgroups': subgroups
                }

                return jsonify(consolidated_data), 200

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + \
                    fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 500,
                    "message": "Error consolidating group and subgroup info: " + ex_str
                }), 500
        
        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

# Define your models
enrollment_model = api.model('Enrollment', {
    'userId': fields.Integer(required=True, description='User ID'),
    'subGroupId': fields.Integer(required=True, description='SubGroup ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
})

message_model = api.model('Message', {
    'message': fields.String(description='Response message'),
})

# Replace @app.route with @api.route and define your endpoint as a Resource
@api.route('/enrollment')
class Enrollment(Resource):
    @api.doc('notify_admin')
    @api.expect(enrollment_model)
    @api.marshal_with(message_model) 
    def post(self):
        user_id = request.json.get('userId')
        subgroup_id = request.json.get('subGroupId')
        username = request.json.get('username')
        email = request.json.get('email')
        # # Create a connection and channel to RabbitMQ
        # connection = create_connection()
        # channel = create_channel(connection)

        # # Create the exchange and queues if they don't exist
        # create_exchange(channel, exchangename, exchangetype)
        # create_queues(channel, exchangename, queue_names, routing_keys)

        # 1. Call [GET] subgroup API from subgroup microservice to check if there is space in the subgroup
        try:
            subgroup_response = requests.get(f'{subgroup_microservice_base_url}/{subgroup_id}', headers={"X-SubGroup-AppId": os.getenv("X_SubGroup_AppId"), "X-SubGroup-Key": os.getenv("X_SubGroup_Key")})
            if subgroup_response.json()['SubGroup']['size'] == len(subgroup_response.json()['SubGroup']['subGroupUsers']):
                return {'message': 'Subgroup is full'}, 400

            groupId = subgroup_response.json()['SubGroup']['groupId']

            # 2. Call [PUT] update subgroup API from subgroup microservice to add user into the subgroup
            update_subgroup_response = requests.put(f'{subgroup_microservice_base_url}/enrol/{subgroup_id}', json={'userId': user_id, 'subGroupId':subgroup_id, 'username': username, 'email': email}, headers={"X-SubGroup-AppId": os.getenv("X_SubGroup_AppId"), "X-SubGroup-Key": os.getenv("X_SubGroup_Key")})



            # 3. Publish user enrollment event to log_queue
            # channel.basic_publish(exchange=exchangename, routing_key=routing_keys[1], body=f"User {user_id} has been enrolled in subgroup {subgroup_id}")

            # Connect to RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters
                            (host=rabbitmq_host_log, port=rabbitmq_port_log,
                            heartbeat=3600, blocked_connection_timeout=3600))
            channel = connection.channel()

            # Defining message 
            message = {
                "log type": "User enrolled", 
                "description": f"{user_id} has been enrolled in subgroup {subgroup_id}",
            }

            # Send message to exchange
            channel.basic_publish(
                exchange=rabbitmq_exchange_log,
                routing_key=rabbitmq_routing_key_log,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2, # make message persistent
                )
            )
            
            # Close the connection when done
            connection.close()

            # 4. If all users in group have been enrolled, publish all user enrollment event to email_queue
            # if all(user['enrolled'] for user in update_subgroup_response.json()['users']):
            count = 0
            group_subgroup_response = requests.get(f'{subgroup_microservice_base_url}/groupsubgroup/{groupId}', headers={"X-SubGroup-AppId": os.getenv("X_SubGroup_AppId"), "X-SubGroup-Key": os.getenv("X_SubGroup_Key")})
            for subgroup in group_subgroup_response.json()['GroupSubGroup']['subGroups']:
                if subgroup['size'] == len(subgroup['subGroupUsers']):
                    count += 1
            if count == len(group_subgroup_response.json()['GroupSubGroup']['subGroups']):
                # channel.basic_publish(exchange=exchangename, routing_key=routing_keys[0], body="All users in group have been enrolled")
                grp_name, creator_email = get_creator_email(groupId)

                # Connect to RabbitMQ
                connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=rabbitmq_host_notif, port=rabbitmq_port_notif,
                                heartbeat=3600, blocked_connection_timeout=3600))
                channel = connection.channel()

                subject = f"[TaskMaster] All projects in community {grp_name} are full."
                body = f"Hello {email}," + f"\n\nAll projects in {grp_name} are currently full. If you want more users to be involved in projects within the community you have created, please add a new project. Thank you. \n\nBest regards,\nTaskMaster"
                
                # Defining message 
                message = {
                    "recipient": creator_email,
                    "subject": subject,
                    "body": body
                }

                # Send message to exchange
                channel.basic_publish(
                    exchange=rabbitmq_exchange_notif,
                    routing_key=rabbitmq_routing_key_notif,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2, # make message persistent
                    )
                )

                # Close the connection when done
                connection.close()

            # 5. If the subgroup is now full after the user has been added, return a message to the user
            updated_subgroup_response = requests.get(f'{subgroup_microservice_base_url}/{subgroup_id}', headers={"X-SubGroup-AppId": os.getenv("X_SubGroup_AppId"), "X-SubGroup-Key": os.getenv("X_SubGroup_Key")})
            if updated_subgroup_response.json()['SubGroup']['size'] == len(updated_subgroup_response.json()['SubGroup']['subGroupUsers']) :
                return {'message': f'Subgroup {subgroup_id} is now full'}, 200


            return {'message': 'User has been enrolled in the subgroup'}, 200

        except:
            return {'message': 'User enrollment failed'}, 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
