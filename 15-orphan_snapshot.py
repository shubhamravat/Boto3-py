import boto3
import datetime
import pytz
from datetime import datetime
aws_mag_con=boto3.session.Session()
aws_ec2_cli=aws_mag_con.client("ec2")
tz = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz)
snap_list=[]
snap_list_new=[]
f1={
            'Name': 'status',
            'Values': [
                'completed',
            ]
        }
response=aws_ec2_cli.describe_snapshots(Filters=[f1],OwnerIds=["532102821576"])
print(response)
for item in response['Snapshots']:
    snap_list.append(item['SnapshotId'])
    date_obj = (item['StartTime'])
    new_date_str = date_obj.strftime("%y-%m-%d")
    if new_date_str<'23-02-16':
        snap_list_new.append(item['SnapshotId'])
        #aws_ec2_cli.deregister_image(ImageId=item['ImageId'])
        #print("deregistering the image {}".format(item['ImageId']))
           
print("list of all snapshot in the account are {} ".format(snap_list))
print("list of all snapshot less then provided date in the account are {} ".format(snap_list_new))
for snap in snap_list_new:
    print(snap)
