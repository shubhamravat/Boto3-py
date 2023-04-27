import boto3
import datetime
import pytz
from datetime import datetime
tz = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz)
current_time_ist = now.strftime('%H:%M')
trigger_time=datetime(2023, 2, 15, 1, 26, 0, tzinfo=tz)
trigger_time_ist=trigger_time.strftime('%H:%M')
instance_lst=[]
def trigger():
    if current_time_ist==trigger_time_ist:
                aws_ec2_con.stop_instances(InstanceIds=instance_lst)
                print("stopping the EC2 with ID as trigger time reached")
    else:
        print("sorry trigger time not matching")


aws_mag_con=boto3.session.Session()
aws_ec2_con=aws_mag_con.client('ec2')
f1={
    "Name":"tag:application name",
    "Values": ['wordpress']

}
response=aws_ec2_con.describe_instances(Filters=[f1])['Reservations']
for each_item in response:
    for each_item2 in each_item['Instances']:
        instance_lst.append(each_item2['InstanceId'])
print(instance_lst)

trigger()
            


        #print(each_item2['InstanceId'],each_item2["PrivateIpAddress"])