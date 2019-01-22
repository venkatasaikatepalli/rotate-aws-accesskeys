# Rotate-aws-keys
to rotate all users acceskeys and sending email to user

## Pre requirements
- IAM role user with only access userdata and generate accesskey.
- installed awscli
- `AccessKeyId`, `SecretAccessKey` added in the running machine

## Steps to start process
```
virtualenv -p python3 ~/env
source ~/env/bin/activate
pip install -r requirements.txt
```

## run process
```
python app.py
```

## security Alert
Never check in any credentials to **Github**

## Author

[Venkata Sai Katepalli - Full Stack Engineer](http://venkatasaikatepalli.github.io)
