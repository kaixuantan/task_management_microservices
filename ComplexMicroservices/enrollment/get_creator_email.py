import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_creator_email(groupId):
    url = f"https://personal-rc7vnnm9.outsystemscloud.com/GroupAPI_REST/rest/v1/group/{groupId}"
    headers = {
        "X-Group-AppId": os.getenv("X_Group_AppId"),
        "X-Group-Key": os.getenv("X_Group_Key"),
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        creatorId = data["Group"]["createdById"]
        name = data["Group"]["name"]
        email = get_user(creatorId)
        return name, email
    else:
        print(f"Failed to fetch group. Status code: {response.status_code}")

def get_user(userId):
    url = f"https://personal-rc7vnnm9.outsystemscloud.com/UserAPI_REST/rest/v1/user/{userId}"
    headers = {
        "X-User-AppId": os.getenv("X_User_AppId"),
        "X-User-Key": os.getenv("X_User_Key"),
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        email = data["User"]["email"]
        return email
    else:
        print(f"Failed to fetch group. Status code: {response.status_code}")   