from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# TO DO: Replace with dynamic user ID 
userId = "1" 
 
# Provided sub group app ID and API key 
sub_group_credentials = { 
    "sub_group_app_id": "dPgLc9FzdypatRXjVJl1", 
    "sub_group_api_key": "jRysav78rLvL7hgfSBGG1MuRuDjMaU" 
} 
 
# URLs for simple microservices 
subgroup_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup" 
user_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/UserAPI_REST/rest/v1/user" 
group_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/GroupAPI_REST/rest/v1/"
log_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/LogAPI_REST/rest/v1/"
notification_microservice_base_url = ""

# Part 1 (1 to 3 or 16 to 19)
@app.route("/enrollment/subgroups") 
def get_subgroups_of_group(): 
    response = requests.get(f"{group_microservice_base_url}/usergroup/{userId}") 
 
    if response.status_code == 200: 
        consolidated = {} 
        # for each group in response, get subgroups of group 
        # TO DO: Edit code based on actual response structure 
        for group in response.json(): 
            groupId = group["groupId"] 
            response2 = requests.get(f"{subgroup_microservice_base_url}/groupsubgroup/{groupId}") 
            consolidated[groupId] = response2.json() 
         
        return jsonify(consolidated) 
     

    else:
        return jsonify({"error": "Failed to get user groups"}), response.status_code


# Part 2
@app.route('/enroll', methods=['POST'])
def enroll_user():
    user_id = request.json.get('userId')
    subgroup_id = request.json.get('subGroupId')
    group_id = request.json.get('groupId')

    # 1. Call [GET] get user's groups API from group microservice to get user groups
    user_groups_response = requests.get(f'{group_microservice_base_url}/groups/{user_id}')
    user_groups = user_groups_response.json()

    # 2. For each group user is in, call [GET] get group's subgroup API from subgroup microservice to get subgroups of the group
    subgroups = []
    for group in user_groups:
        subgroup_response = requests.get(f'{subgroup_microservice_base_url}/subgroups/{group_id}')
        subgroups.extend(subgroup_response.json())

    # 3. Consolidate list of groups and subgroups and return to UI
    consolidated_data = {
        'userGroups': user_groups,
        'subgroups': subgroups
    }

    # 4. Call [PUT] update subgroup API from subgroup microservice to add user into the subgroup
    update_subgroup_response = requests.put(f'{subgroup_microservice_base_url}/subgroups/{subgroup_id}', json={'userId': user_id})

    # 5. If all users in group have been enrolled, call notification microservice to notify admin
    if all(user['enrolled'] for user in update_subgroup_response.json()['users']):
        requests.post(f'{notification_microservice_base_url}/notify', json={'message': 'All users have been enrolled in the subgroup'})

    # 6. Call [POST] add log API from activity log microservice to record enrolment of user to subgroup
    requests.post(f'{log_microservice_base_url}/logs', json={'userId': user_id, 'subgroupId': subgroup_id, 'action': 'enroll'})

    return jsonify(consolidated_data), 200

if __name__ == '__main__':
    app.run(debug=True)