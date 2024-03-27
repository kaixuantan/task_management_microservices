from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import json
from process_pdf import process_pdf
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/ideas/generate/<subGroupId>', methods=['GET'])
def generate_ideas(subGroupId):
    # Here you can add the functionality you want.
    # For example, let's return a simple JSON response.
    
    text = process_pdf(subGroupId)
    print(text)
    data = {
                "document": text,
                "subGroupId": subGroupId,
                "type": "md",
            }
    return upload_file(subGroupId, "md", data)
    

@app.route('/ideas/upload', methods=['POST'])
def upload():
    data = request.get_json()
    subGroupId = data['subGroupId']
    fileType = data['type']
    
    return upload_file(subGroupId, fileType, data)

def upload_file(subGroupId, fileType, fileData):
    headers = {
        'Content-Type': 'application/json',
        "X-Doc-AppId": os.getenv("X_Doc_AppId"),
        "X-Doc-Key": os.getenv("X_Doc_Key"),
    }
    file_exists = check_file_exist(subGroupId, fileType)
    try:
        if file_exists:
            docId = file_exists
            url = f"https://personal-rc7vnnm9.outsystemscloud.com/DocAPI_REST/rest/v1/doc/{docId}"
            response = requests.put(url, headers=headers, data=json.dumps(fileData))
        else:
            url = "https://personal-rc7vnnm9.outsystemscloud.com/DocAPI_REST/rest/v1/doc/"
            response = requests.post(url, headers=headers, data=json.dumps(fileData))
        return response.json()
    except Exception as error:
        print(error)
        return {"error": "Failed to upload file"}

def check_file_exist(subGroupId, fileType):
    url = f"https://personal-rc7vnnm9.outsystemscloud.com/DocAPI_REST/rest/v1/doc/subgrouptype/{subGroupId}"
    headers = {
        "X-Doc-AppId": os.getenv("X_Doc_AppId"),
        "X-Doc-Key": os.getenv("X_Doc_Key"),
        "type": fileType,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data["Result"]["Success"]:
        return data["DocAPI"]["docId"]
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)