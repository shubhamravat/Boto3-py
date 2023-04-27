import boto3
import csv

aws_mag_con = boto3.session.Session()
aws_ec2_cli = aws_mag_con.client("ec2")
csv_ob=open("unattached_inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_No","Volume_Id","VolumeSize(GB)","Volume Type"])
count=1
response = aws_ec2_cli.describe_volumes()
#print(response)
#print(response["Volumes"]) 
unattached_ebs_list=[]
for item in response["Volumes"]:
    if len(item['Attachments'])==0:
        print(item['VolumeId'])
        csv_w.writerow([count,item['VolumeId'],item['Size'],item['VolumeType']])
        unattached_ebs_list.append(item['VolumeId'])
        count=count+1

csv_ob.close()