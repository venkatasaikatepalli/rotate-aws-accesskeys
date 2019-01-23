import boto3
import json
import flask
from flask import Flask, render_template
from botocore.exceptions import ClientError

__author__ = "Venkata.Sai.Kateppalli<venkatasaikatepalli@gmail.com>"
__version__ = "1.0"


class IAMManager():
    def __init__(self):
        self.client = boto3.client('iam')
        self.email_client = boto3.client('ses')
        self.auth_user = boto3.client('sts').get_caller_identity()
    
    # list all users associated with this account
    def get_users(self):
        users = self.client.list_users()
        return users['Users']
    
    # refresh all users and keys associated with this account
    def refresh_keys(self, user, delete=True):
        keys = {
            'old_keys': self.client.list_access_keys(
                UserName=user['UserName']
            )['AccessKeyMetadata'],
            'new_keys': {}
        }
        # if delete true
        if delete is True:
            for idx, key in enumerate(keys['old_keys']):
                if key['AccessKeyId'] != "AKIAJFH72J3CEFBBNIZQ":
                    response = self.client.delete_access_key(
                        UserName=key['UserName'],
                        AccessKeyId=key['AccessKeyId']
                    )
                    if response['ResponseMetadata']['HTTPStatusCode'] is 200:
                        keys['old_keys'][idx].update({
                            'deleted': True
                        })
        # create new keys
        new_key = self.client.create_access_key(
            UserName=user['UserName']
        )
        if new_key['ResponseMetadata']['HTTPStatusCode'] is 200:
            keys.update({
                'new_keys': new_key['AccessKey']
            })
        return keys
    
    def send_email(self, user):
        RECIPIENT = "<email_address>"
        AWS_REGION = "us-east-1"
        SUBJECT = "{} AWS Accesskey Rotation".format(user["UserName"])
        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Welcome user")
        # The HTML body of the email.
        BODY_HTML = render_template('email.html', user=user)
        # The character encoding for the email.
        CHARSET = "UTF-8"
        SENDER = "<email_address>"
        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = self.email_client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    # rotate keys
    def rotate_user_keys(self):
        response = []
        # loop users
        for user in self.get_users():
            if user['UserId'] != self.auth_user['UserId']:
                user.update({
                    'accesskeys': self.refresh_keys(user)
                })
                self.send_email(user)
            response.append(user)
        return flask.jsonify(response)