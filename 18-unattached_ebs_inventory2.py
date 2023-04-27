import boto3
import csv

csv_ob=open("ebs_inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_No","Instance_Id","VolumeId","State","VolumeSize","VolumeType"])

aws_mag_con = boto3.session.Session()
aws_ec2_cli = aws_mag_con.client("ec2")
response = aws_ec2_cli.describe_volumes()
all_vol_list=[]
unused_vol_list=[]
count=0
for item in response["Volumes"]:
    count=count+1
    if "Attachments" in item and item["Attachments"]:
        instance_id = item["Attachments"][0]["InstanceId"]
    else:
        instance_id = "NA"

    print(count,instance_id, item["VolumeId"], item['State'], item['Size'], item["VolumeType"])
    csv_w.writerow([count,instance_id, item["VolumeId"], item['State'], item['Size'], item["VolumeType"]])
    
csv_ob.close()