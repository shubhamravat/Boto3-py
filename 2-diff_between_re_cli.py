#### listing users with resource object

import boto3
aws_mag_con=boto3.session.Session()
iam_console=aws_mag_con.resource("iam")
print("\n============================IAM user names ===================")

for each_user in iam_console.users.all():
    print(each_user.name)

#### listing users with client object

import boto3
aws_mag_con=boto3.session.Session()
iam_console_cli=aws_mag_con.client("iam")
respons= iam_console_cli.list_users()
for each_item in respons['Users']:
    print(each_item['UserName'])

    