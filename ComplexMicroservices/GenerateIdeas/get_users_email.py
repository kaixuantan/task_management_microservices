import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_users_email(subGroupId):
    url = f"https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/subgroup/{subGroupId}"
    headers = {
        "X-SubGroup-AppId": os.getenv("X_SubGroup_AppId"),
        "X-SubGroup-Key": os.getenv("X_SubGroup_Key"),
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        emails = []
        for user in data["SubGroup"]["subGroupUsers"]:
            emails.append(user["email"])
        return emails
    else:
        print(f"Failed to fetch user emails. Status code: {response.status_code}")   