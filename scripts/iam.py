import boto3
import json
import flask

__author__ = "Venkata.Sai.Kateppalli<venkatasaikatepalli@gmail.com>"
__version__ = "1.0"


class IAMManager():
    def __init__(self):
        self.client = boto3.client('iam')
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
    
    # rotate keys
    def rotate_user_keys(self):
        response = []
        # loop users
        for user in self.get_users():
            if user['UserId'] != self.auth_user['UserId']:
                user.update({
                    'keys': self.refresh_keys(user)
                })
            response.append(user)
        return flask.jsonify(response)