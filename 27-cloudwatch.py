#cloudwatch log archival to s3 which are older than 90 days

import boto3
import datetime
import time
import pytz
today = datetime.datetime.now().date()
aws_mag_con=boto3.session.Session()
aws_cloudwatch_con=aws_mag_con.client('logs')
aws_s3_con=aws_mag_con.client('s3')

log_list=[]

response=aws_cloudwatch_con.describe_log_groups()['logGroups']
from_time = 0
to_time = today

for item in response:
    #print(item['creationTime'])
    date = datetime.datetime.fromtimestamp(item['creationTime'] / 1000.0)

# Format the datetime object as a string
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    #print(formatted_date,item['logGroupName'])
    log_list.append(item['logGroupName'])
    if formatted_date=='2022-05-16 20:12:04':
        print(f"date  match for logs {item['logGroupName']}")
        aws_cloudwatch_con.create_export_task(
    taskName='s3-upload-logs',
    logGroupName=item['logGroupName'],
    destinationPrefix='/logs',
    fromTime=from_time,
    to=int(time.time() * 1000),
    destination='shubham-portfolio'
)
print(log_list)


'''
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "AllowCloudWatchLogsAccess",
			"Effect": "Allow",
			"Principal": {
				"Service": "logs.ap-south-1.amazonaws.com"
			},
			"Action": [
				"s3:GetBucketAcl",
				"s3:GetBucketLocation",
				"s3:*"
			],
			"Resource": [
				"arn:aws:s3:::shubham-portfolio/*",
				"arn:aws:s3:::shubham-portfolio"
			]
		},
		{
			"Sid": "AllowCloudWatchLogsPutObject",
			"Effect": "Allow",
			"Principal": {
				"Service": "logs.ap-south-1.amazonaws.com"


'''
    

 I have successfully deployed a static website on Amazon S3 and mapped a custom domain to the S3 website endpoint. The website is accessible via the custom domain and is fully functional. I am currently working on adding more features to the website to improve its functionality a



