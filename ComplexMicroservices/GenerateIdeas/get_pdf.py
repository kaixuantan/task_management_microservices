import requests
from dotenv import load_dotenv
import os
import base64

load_dotenv()

def download_pdf(subGroupId):
    url = f"https://personal-rc7vnnm9.outsystemscloud.com/DocAPI_REST/rest/v1/doc/subgrouptype/{subGroupId}"
    headers = {
        "X-Doc-AppId": os.getenv("X_Doc_AppId"),
        "X-Doc-Key": os.getenv("X_Doc_Key"),
        "type": "pdf",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        pdf_data = base64.b64decode(data['DocAPI']['document'])
        return pdf_data
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
