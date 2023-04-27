'''
import boto3
aws_mag_con=boto3.session.Session()
iam_con_cli=aws_mag_con.client(service_name="iam",region_name="ap-south-1")
response=iam_con_cli.list_users()
for each_item in response['Users']:
    print(each_item['Username'])
    '''

import boto3
aws_mag_con=boto3.session.Session()
iam_console=aws_mag_con.resource("iam")
print("\n============================IAM user names ===================")

for each_user in iam_console.users.all():
    print(each_user.name)
print("\n============================bucket names ===================")

aws_mag_con=boto3.session.Session()
s3_console=aws_mag_con.resource("s3")
for each_bucket in s3_console.buckets.all():
    print(each_bucket)