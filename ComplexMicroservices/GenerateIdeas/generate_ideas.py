from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import json
import requests
import os

from process_pdf import process_pdf
from send_amqp import *
from get_users_email import get_users_email

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

ns = api.namespace('ideas', description='Operations related to idea generation and project summary')

# Define your response fields
result_model = api.model('Result', {
    'Success': fields.Boolean,
    'ErrorMessage': fields.String
})

resource_fields = api.model('Resource', {
    'DocId': fields.String,
    'Result': fields.Nested(result_model)
})

@ns.route('/generate/<subGroupId>/<userId>')
class IdeaGeneration(Resource):
    @api.doc(params={'subGroupId': 'subGroupId of project that the pdf belongs to', 'userId': 'The user who uploaded the pdf'})
    @api.marshal_with(resource_fields) 
    def get(self, subGroupId, userId):
        # Here you can add the functionality you want.
        # For example, let's return a simple JSON response.
        
        text = process_pdf(subGroupId)
        # print(text)
        data = {
                    "document": text,
                    "subGroupId": subGroupId,
                    "type": "md",
                }
        return upload_file(subGroupId, "md", data, userId)
    

upload_model = api.model('Upload', {
    'subGroupId': fields.Integer(required=True, description='Subgroup ID'),
    'type': fields.String(required=True, description='File type'),
    'document': fields.String(required=True, description='Document content'),
})

@ns.route('/upload')
class IdeaUpload(Resource):
    @api.expect(upload_model, validate=True)
    @api.marshal_with(resource_fields)
    def post(self):
        data = api.payload
        subGroupId = data['subGroupId']
        fileType = data['type']
        
        return upload_file(subGroupId, fileType, data, None)

def upload_file(subGroupId, fileType, fileData, userId):
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
    except Exception as error:
        print(f"Error: {error}")
        return {"Result": {"Success": False, "ErrorMessage": "Failed to upload file"}}
    
    if response and fileType == "md":
        # Notification and Logging
        try:
            connection, channel = open_connection()
            notify_users(subGroupId, channel)
            send_log(subGroupId, userId, "Generate ideas", f"{userId} generated ideas and project summary for {subGroupId}", channel)
            close(connection)
        except Exception as error:
            print(f"Error: {error}")
            return {"Result": {"Success": False, "ErrorMessage": "Failed to notify users or do logging"}}
    
    if response:
        return response.json()

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

def notify_users(subGroupId, channel):
    emails = get_users_email(subGroupId)
    for email in emails:
        send_notif(email, "Project summary and ideas generated successfully!", "Head to the project page to view the details. Feel free to Upload a new PDF file to generate the response again. \nDisclaimer: Content generated using AI, please check for accuracy.", channel)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)