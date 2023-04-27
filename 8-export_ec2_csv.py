import boto3
import csv
aws_mag_con=boto3.session.Session()
aws_ec2_cli=aws_mag_con.client("ec2")
csv_ob=open("ec2_inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_No","Instance_Id","Instance_Type","Private_Ip_Address",'State',"Architecture"])
count=1
response=aws_ec2_cli.describe_instances()
for each_item in response['Reservations']:
    for each_instance in each_item['Instances']:
        print(count,each_instance['InstanceId'],each_instance['InstanceType'],each_instance['PrivateIpAddress'],each_instance['State']['Name'],each_instance['Architecture'])
        csv_w.writerow([count,each_instance['InstanceId'],each_instance['InstanceType'],each_instance['PrivateIpAddress'],each_instance['State']['Name'],each_instance['Architecture']])
        count=count+1
csv_ob.close()   