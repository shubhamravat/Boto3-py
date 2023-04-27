import boto3

aws_mag_con = boto3.session.Session()
aws_ec2_cli = aws_mag_con.client("ec2")
response = aws_ec2_cli.describe_volumes()
all_vol_list=[]
unused_vol_list=[]

for item in response["Volumes"]:
    if "Attachments" in item and item["Attachments"]:
        instance_id = item["Attachments"][0]["InstanceId"]
    else:
        instance_id = "NA"
        unused_vol_list.append(item["VolumeId"])
    #result=instance_id, item["VolumeId"], item['State'], item['Size'], item["VolumeType"]
   


for items in response["Volumes"]:
     all_vol_list.append(items["VolumeId"])


print(all_vol_list)    

print(unused_vol_list)
