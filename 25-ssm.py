import boto3
import pandas as pd

aws_mag_con = boto3.session.Session()
aws_ec2_con = aws_mag_con.client("ec2")
aws_s3_con = aws_mag_con.client("s3")
ssm = aws_mag_con.client("ssm")

response = aws_ec2_con.describe_instances()["Reservations"]
instance_list = []
count = 1
hostname_error = "NA"

# Create a dataframe to hold the instance data
data = {"S_No": [], "Host": [], "Instance Id": [], "State": [], "Instance Type": [], "AZ": [], "Private IP": [], "VPC ID": [], "SubnetID": []}
df = pd.DataFrame(data)

for item in response:
    for each in item["Instances"]:
        instance_list.append(each["InstanceId"])

for instance_id in instance_list:
        instance = aws_ec2_con.describe_instances(InstanceIds=[instance_id])["Reservations"][0]["Instances"][0]
        #print(instance['Tags']['Name'])
        for tag in instance['Tags']:
            if tag['Key'] =='Name':
               print(tag['Value'])
#print(instance)       
 