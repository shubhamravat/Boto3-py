import boto3
import datetime
import pytz
from datetime import datetime
import csv



aws_mag_console=boto3.session.Session()
aws_iam_con=aws_mag_console.client('iam')
response=aws_iam_con.list_users()
#print(response)
csv_ob=open("iam_inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_No","UserName","Arn","PolicyName","Creation Date"])
count=1

for each_item in response['Users']:
    creation_date = each_item['CreateDate']
    creation_date = creation_date.replace(tzinfo=pytz.UTC)
    creation_date = creation_date.astimezone(pytz.timezone('Asia/Kolkata'))
    print(each_item['UserName'],each_item['Arn'],creation_date)
    policy1=aws_iam_con.list_attached_user_policies(UserName=each_item['UserName'])['AttachedPolicies']
   # for policies in policy1:
   #     print(policies['PolicyName'])
    #    csv_w.writerow([count,each_item['UserName'],each_item['Arn'],policies['PolicyName'],creation_date])
    policy_names = []
    for policy in policy1:
        policy_names.append(policy['PolicyName'])

    policy_names = ', '.join(policy_names)

    csv_w.writerow([count,each_item['UserName'],each_item['Arn'],policy_names,creation_date])


    count=count+1

csv_ob.close()

    
