import uuid
import requests
from flask import Flask, request, jsonify

# Initialize Flask application
app = Flask(__name__)

# Provided sub group app ID and API key
sub_group_credentials = {
    "sub_group_app_id": "dPgLc9FzdypatRXjVJl1",
    "sub_group_api_key": "jRysav78rLvL7hgfSBGG1MuRuDjMaU"
}

# Base URL for the subgroup microservice
subgroup_microservice_base_url = "https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup"


# Route to create subgroups by the admin
@app.route("/subgroup", methods=["POST"])
def create_subgroup():
    data = request.get_json()
    admin_id = data.get("admin_id")
    group_name = data.get("group_name")
    num_subgroups = data.get("num_subgroups")
    subgroup_capacity = data.get("subgroup_capacity", 10)  # Default capacity is 10

    # Validate input data
    if not admin_id or not group_name or not num_subgroups:
        return jsonify({"error": "Missing required fields"}), 400

    # Create subgroups
    for _ in range(num_subgroups):
        subgroup_id = str(uuid.uuid4())
        subgroup_data = {
            "groupId": admin_id,
            "name": f"{group_name} Subgroup",
            "size": 0,
            "subGroupUsers": []
        }
        response = requests.post(f"{subgroup_microservice_base_url}/", json=subgroup_data, headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
        if response.status_code != 200:
            return jsonify({"error": "Failed to create subgroups"}), response.status_code

    return jsonify({"message": "Subgroups created successfully"})

# Route to get all subgroups
@app.route("/subgroup", methods=["GET"])
def get_all_subgroups():
    response = requests.get(subgroup_microservice_base_url, headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get subgroups"}), response.status_code

# Route to get a specific subgroup
@app.route("/subgroup/<subgroup_id>", methods=["GET"])
def get_subgroup(subgroup_id):
    response = requests.get(f"{subgroup_microservice_base_url}/{subgroup_id}", headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
    if response.status_code == 200:
        return jsonify(response.json())
    elif response.status_code == 404:
        return jsonify({"error": "Subgroup not found"}), 404
    else:
        return jsonify({"error": "Failed to get subgroup"}), response.status_code

# Route to update subgroup
@app.route("/subgroup/<subgroup_id>", methods=["PUT"])
def update_subgroup(subgroup_id):
    data = request.get_json()
    subgroup_name = data.get("name")
    if not subgroup_name:
        return jsonify({"error": "Missing name field"}), 400

    response = requests.put(f"{subgroup_microservice_base_url}/{subgroup_id}", json={"name": subgroup_name}, headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
    if response.status_code == 200:
        return jsonify({"message": "Subgroup updated successfully"})
    elif response.status_code == 404:
        return jsonify({"error": "Subgroup not found"}), 404
    else:
        return jsonify({"error": "Failed to update subgroup"}), response.status_code

# Route to delete subgroup
@app.route("/subgroup/<subgroup_id>", methods=["DELETE"])
def delete_subgroup(subgroup_id):
    response = requests.delete(f"{subgroup_microservice_base_url}/{subgroup_id}", headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
    if response.status_code == 200:
        return jsonify({"message": "Subgroup deleted successfully"})
    elif response.status_code == 404:
        return jsonify({"error": "Subgroup not found"}), 404
    else:
        return jsonify({"error": "Failed to delete subgroup"}), response.status_code

# Route to self-enroll user to subgroup
@app.route("/subgroup/enrol/<subgroup_id>/<user_id>", methods=["PUT"])
def self_enrol_user_to_subgroup(subgroup_id, user_id):
    response = requests.put(f"{subgroup_microservice_base_url}/enrol/{subgroup_id}/{user_id}", headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
    if response.status_code == 200:
        return jsonify({"message": "User enrolled to subgroup successfully"})
    elif response.status_code == 400:
        return jsonify({"error": "Subgroup is full. Enrollment failed."}), 400
    else:
        return jsonify({"error": "Failed to enroll user to subgroup"}), response.status_code

# Route to get group's subgroups
@app.route("/subgroup/groupsubgroup/<group_id>", methods=["GET"])
def get_group_subgroups(group_id):
    response = requests.get(f"{subgroup_microservice_base_url}/groupsubgroup/{group_id}", headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get group's subgroups"}), response.status_code

# Route to get user's subgroups
@app.route("/subgroup/usersubgroup/<user_id>", methods=["GET"])
def get_user_subgroups(user_id):
    response = requests.get(f"{subgroup_microservice_base_url}/usersubgroup/{user_id}", headers={"X-SubGroup-AppId": sub_group_credentials["sub_group_app_id"], "X-SubGroup-Key": sub_group_credentials["sub_group_api_key"]})
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get user's subgroups"}), response.status_code

# Main function to run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
