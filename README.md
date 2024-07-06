Details of automation project worked so far -


Automation in Cloud
● Use SDK for python (boto3) to automate the 
infrastructure.

● AWS integration with fresh service and jira ticketing 
tool

● Phone call automation on receiving AWS alerts.

● Building a Custom Security Alert System with Lambda , 
CloudTrail and SES which will Automatically Revoke 
Unauthorized Inbound Rules .

● Created python boto3 script which automated manual 
task of updating parameter store value in bulk with help 
of excel sheet.

● Created Excel format inventory of all EC2 instance id, 
instance type, its state, Private

● I.P address with help of python boto3

● Start and stop 200+ EC2 instances in Prod and
non-Prod automatically on trigger time as per the tag

● Created list of all unused/unattached EBS volume with 
its type (gp2, gp3) and delete it automatically

● Created list of all snapshot that are unattached to AMI 
(orphan Snapshot)

● Deregister AMI on or before a specific date

● Created an alert with help of python boto3 that trigger 
right before 15 days of expiration of any ACM 
certificate in AWS account

● Created an alert with help of python boto3 that trigger 
right after 60 days of creation of Access Key in IAM 
and then rotate it by creating new access key after 
disabling older one and send new one to user directly 
via mail
