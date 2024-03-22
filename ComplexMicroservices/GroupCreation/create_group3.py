from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import pika
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# URLs
group_URL = "https://personal-rc7vnnm9.outsystemscloud.com/GroupAPI_REST/rest/v1/group/"
subgroup_URL = "https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup/"
activity_log_URL = "https://personal-rc7vnnm9.outsystemscloud.com/LogAPI_REST/rest/v1/log/"
user_URL = "https://personal-rc7vnnm9.outsystemscloud.com/UserAPI_REST/rest/v1/user/"


# Group Creation complex microservice

@app.route("/create_group3", methods=['POST'])
def group_creation():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            group_info = request.get_json()[0] #only name is mandatory
            print("\nReceived a group_description in JSON:", group_info)
            subgroup_info = request.get_json()[1] #only name is mandatory
            print("\nReceived a list of subgroups in JSON:", subgroup_info)
            users_id_list = request.get_json()[2] #list of userId
            print("\nReceived a list of usersId in JSON:", users_id_list) 

            # Send group info 
            result = processGroupCreation(group_info,subgroup_info,users_id_list)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_group.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processGroupCreation(group_info,subgroup_info,users_id_list):
    # Send the group info
    # Invoke the group microservice

    print('\n-----Invoking group microservice-----')
    group_headers = {'X-Group-AppId': request.headers.get('X-Group-AppId'), "X-Group-Key": request.headers.get('X-Group-Key')}
    # create a group in group microservice
    group_result = invoke_http(group_URL, method="POST", json=group_info, headers=group_headers)
    # print(group_result)
    group_result_status = group_result["Result"]
    groupId = group_result["GroupId"]
    # print(groupId)
    print('group_result:', group_result_status) # creation successful

    # get group details 
    unique_group_URL = group_URL + str(groupId)
    # print(unique_group_URL)
    group_dict = invoke_http(unique_group_URL, method="GET", headers=group_headers)
    # print(group_dict)
    group = group_dict["Group"]
    # print(group)

    # Record new group in activity logs
    print('\n\n-----Invoking activity_log microservice-----')
    log_headers = {'X-Log-AppId': request.headers.get('X-Log-AppId'), "X-Log-Key": request.headers.get('X-Log-Key')}
    invoke_http(activity_log_URL, method="POST", json=group, headers=log_headers)
    print("\nGroup sent to activity log.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails

    # create new subgroup in group 
    # Invoke the subgroup microservice
    
    for i in range(len(subgroup_info)): 
        print('\n\n-----Invoking subgroup microservice-----')
        subgroup_headers = {'X-SubGroup-AppId': request.headers.get('X-SubGroup-AppId'), "X-SubGroup-Key": request.headers.get('X-SubGroup-Key')}
        # create subgroup
        subgroup_result = invoke_http(subgroup_URL, method="POST", json=subgroup_info[i], headers=subgroup_headers)
        # print(subgroup_result)
        subgroup_result_status = subgroup_result["Result"]
        subGroupId = subgroup_result["SubGroupId"]
        print("subgroup_result:", subgroup_result_status, '\n') # creation successful

        # get subgroup details
        unique_subgroup_URL = subgroup_URL + str(subGroupId)
        subgroup_dict = invoke_http(unique_subgroup_URL, method="GET", headers=subgroup_headers)
        subgroup = subgroup_dict["SubGroup"]

            #invoke notification
        # RabbitMQ connection details
        rabbitmq_host = os.getenv('HOSTNAME')
        rabbitmq_port = os.getenv('PORT')
        rabbitmq_exchange = os.getenv('EXCHANGE_NAME')
        rabbitmq_exchange_type = os.getenv('EXCHANGE_TYPE') 
        rabbitmq_queue = os.getenv('QUEUE_NAME')
        rabbitmq_routing_key = os.getenv('ROUTING_KEY')  

        # Email server details
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')

        test_email = os.getenv('TEST_EMAIL')

        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters
                                            (host=rabbitmq_host, port=rabbitmq_port,
                                            heartbeat=3600, blocked_connection_timeout=3600))
        channel = connection.channel()

        # Define the message
        message = {
            "recipient": test_email,
            "subject": "Community Created",
            "body": "Dear user, you have been assigned to a community. Please proceed to enter a subgroup"
        }

        # Send the message to the exchange
        channel.basic_publish(
            exchange=rabbitmq_exchange,
            routing_key=rabbitmq_routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2, # make message persistent
            )
        )

        print(f"Message sent to the exchange '{rabbitmq_exchange}' with routing key '{rabbitmq_routing_key}'.")

        # Close the connection
        connection.close()

        # Record new subgroup in logs
        print('\n\n-----Invoking activity_log microservice-----')
        headers = {'X-Log-AppId': request.headers.get('X-Log-AppId'), "X-Log-Key": request.headers.get('X-Log-Key')}
        invoke_http(activity_log_URL, method="POST", json=subgroup, headers=log_headers)
        print("\nSubgroup ",i, " sent to activity log.\n")
        # - reply from the invocation is not used;
        # continue even if this invocation fails

    #assign users to group
    assigned_group = processUserAssignment(group,users_id_list)
    updated_group_result_status = invoke_http(unique_group_URL, method="PUT", json=assigned_group, headers=group_headers)
    print("updated_group_result_status: ", updated_group_result_status)

    # Return created group, subgroup, assigned_group
    return {
        "code": 201,
        "data": {
            "subgroup_result": subgroup,
            "final_group_result": assigned_group
        }
    }

# User Group Assignment complex microservice
def processUserAssignment(group,user_id_list):
    groupId = group['groupId']
    users_assigned = [] # list of users assigned
    if len(user_id_list) <= group['size']:
        for id in user_id_list:
            print(id)
            user_headers = {'X-User-AppId': request.headers.get('X-User-AppId'), "X-User-Key": request.headers.get('X-User-Key')}
            unique_user_URL = user_URL + str(id)
            user_dict = invoke_http(unique_user_URL, method="GET", headers=user_headers)
            print(user_dict)
            user = user_dict["User"]
            username = user["username"]
            assignee = {
                "groupId": groupId,
                "userId": id,
                "username": username
            }
            print(assignee)
            users_assigned.append(assignee)

    group_headers = {'X-Group-AppId': request.headers.get('X-Group-AppId'), "X-Group-Key": request.headers.get('X-Group-Key')}
    assign_users_URL = group_URL + "/assign/" + str(groupId)
    assigned_user_status = invoke_http(assign_users_URL, method="PUT", json=users_assigned, headers=group_headers) 
    print("assigned_user_status: ", assigned_user_status)

    # get new group
    unique_group_URL = group_URL + str(groupId) 
    new_group_dict = invoke_http(unique_group_URL, method="GET", headers=group_headers)
    group = new_group_dict["Group"]
    print("new group: ", group, '\n')
    
    # Record group with assigned users in activity logs
    print('\n\n-----Invoking activity_log microservice-----')
    log_headers = {'X-Log-AppId': request.headers.get('X-Log-AppId'), "X-Log-Key": request.headers.get('X-Log-Key')}
    invoke_http(activity_log_URL, method="POST", json=group, headers=log_headers)
    print("\nGroup with users assigned sent to activity log.\n")

    return group
        

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for creating a group...")
    app.run(host="0.0.0.0", port=5100, debug=True)