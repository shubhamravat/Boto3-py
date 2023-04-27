import boto3
import datetime
import pytz
from datetime import datetime
aws_mag_con=boto3.session.Session()
aws_ec2_cli=aws_mag_con.client("ec2")
tz = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz)
current_time_ist = now.strftime('%H:%M')
#trigger_time=datetime(2023, 2, 15, 1, 26, 0, tzinfo=tz)
#trigger_time_ist=trigger_time.strftime('%H:%M')
instance_lst=[]
f1={
    "Name":"tag:Schedule",
    "Values":["True"]
}
response=aws_ec2_cli.describe_instances(Filters=[f1])["Reservations"]
for each in response:
    for each_item in each["Instances"]:
        print(each_item['InstanceId'])
        instance_lst.append(each_item['InstanceId'])
        if current_time_ist=='13:43' and each_item['Tags']=='wordpress':
            aws_ec2_cli.start_instances(InstanceIds=instance_lst)
            print("starting the EC2 with ID as trigger time reached")
        else:
            print("sorry trigger time not matching")
