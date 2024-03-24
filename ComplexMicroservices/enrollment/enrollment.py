from flask import Flask, request, jsonify
import requests

import os
import sys

app = Flask(__name__)

# Provided sub group app ID and API key 
sub_group_credentials = { 
    "sub_group_app_id": "dPgLc9FzdypatRXjVJl1", 
    "sub_group_api_key": "jRysav78rLvL7hgfSBGG1MuRuDjMaU" 
} 

group_credentials = {
    "group_app_id": "fAzGk6o724ynKLjKyM9a",
    "group_api_key": "vODi2UJpYrUMcPRFK4156o2LoR9qSp"
}

# URLs for simple microservices 
subgroup_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup" 
# user_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/UserAPI_REST/rest/v1/user" 
group_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/GroupAPI_REST/rest/v1/group"
# log_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/LogAPI_REST/rest/v1/"
# notification_microservice_base_url = ""


# Part 1: Return consolidated user's group & group's subgroups
@app.route('/enrollment', methods=['GET'])
def get_subgroups_of_group():
    if request.is_json:
        try:    
            user_id = request.json.get('userId')
            group_id = request.json.get('groupId')

            # 1. Call [GET] get user's groups API from group microservice to get user groups
            user_groups_response = requests.get(f'{group_microservice_base_url}/usergroup/{user_id}', headers={"X-Group-AppId": group_credentials["group_app_id"], "X-Group-Key": group_credentials["group_api_key"]})
            user_groups = user_groups_response.json()["UserGroup"]["groups"]

            # 2. For each group user is in, call [GET] get group's subgroup API from subgroup microservice to get subgroups of the group
            subgroups = []
            for group in user_groups:
                group_id = group['groupId']
                subgroup_response = requests.get(f'{subgroup_microservice_base_url}/groupsubgroup/{group_id}', headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
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

    
# Part 2: Enroll user and RabbitMQ
@app.route('/enrollment', methods=['PUT'])
def notify_admin():
    user_id = request.json.get('userId')
    subgroup_id = request.json.get('subGroupId')
    
    # 1. Call [PUT] update subgroup API from subgroup microservice to add user into the subgroup
    try:
        update_subgroup_response = requests.put(f'{subgroup_microservice_base_url}/subgroups/{subgroup_id}', json={'userId': user_id}, headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})

        # 2. If all users in group have been enrolled, publish all user enrollment event to email_queue
        if all(user['enrolled'] for user in update_subgroup_response.json()['users']):
            print("Sending the event to email_queue")

        # 3. Publish user enrollment event to log_queue
        print("Sending the event to log_queue")

        return jsonify({'message': 'User has been enrolled in the subgroup'}), 200

    except:
        return jsonify({'message': 'User enrollment failed'}), 400


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=5009, debug=True)