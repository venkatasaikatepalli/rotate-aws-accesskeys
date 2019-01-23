# Rotate-aws-accesskeys
Rotate aws accesskeys of all users and sending email to user

## Pre-requirements
- IAM role user with only access userdata and generate accesskey.
- installed awscli
- `AccessKeyId`, `SecretAccessKey` added in the running machine

## Ploicy
below access ploicy to be added to `rotate-key-user`
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:DeleteAccessKey",
                "iam:ListUsers",
                "iam:GetUser",
                "iam:ListUserTags",
                "iam:CreateAccessKey"
            ],
            "Resource": "*"
        }
    ]
}
```

## Steps to start process
```
virtualenv -p python3 ~/env
source ~/env/bin/activate
pip install -r requirements.txt
```

## Start server
```
python app.py
```

## <font color="red">Security alert</font>
Never check in any credentials to **Github**

## Author

[Venkata Sai Katepalli - Full Stack Engineer](http://venkatasaikatepalli.github.io)
