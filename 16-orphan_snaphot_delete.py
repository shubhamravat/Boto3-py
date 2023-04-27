import boto3
import datetime
import pytz
from datetime import datetime
aws_mag_con=boto3.session.Session()
aws_ec2_cli=aws_mag_con.client("ec2")
tz = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz)
current_time_ist = now.strftime('%H:%M')
ami_snap_list=[]
total_snap_list=[]
orphan_snap_list=[]
count_orphan=0
count_total=0
count_ami_snap=0
f1={
            'Name': 'status',
            'Values': [
                'completed',
            ]
        }
response_snap=aws_ec2_cli.describe_snapshots(OwnerIds=["532102821576"],Filters=[f1])
response_ami=aws_ec2_cli.describe_images(Owners=["532102821576"])['Images']
for items in response_snap['Snapshots']:
    #print(items["SnapshotId"])
    total_snap_list.append(items["SnapshotId"])

print("=============================check from here===================================================================")
for item in response_ami:
    for each_item in item['BlockDeviceMappings']:
        if 'Ebs' in each_item:
            result=each_item['Ebs']['SnapshotId']
            ami_snap_list.append(result)
print("\nlist of snapshot ami associated with ami =",ami_snap_list)     
print("\nlist of all snapshot =",total_snap_list)       

for snap in total_snap_list:
    if snap not in ami_snap_list:
        orphan_snap_list.append(snap)



        
        
print("\n list of orphan snapshot in account =",orphan_snap_list) 


for orphan_snap in total_snap_list:
    count_total=count_total+1
print("\nCount of all snapshot in account =",count_total)   


for orphan_snap in ami_snap_list:
    count_ami_snap=count_ami_snap+1
print("\nCount of snapshot assosicated with AMI in account =",count_ami_snap)  

for orphan_snap in orphan_snap_list:
    count_orphan=count_orphan+1

print("\nCount of all orphan snapshot in account =",count_orphan)  


for snapshot_id in orphan_snap_list:
    try:
        aws_ec2_cli.delete_snapshot(SnapshotId=snapshot_id)
        print(f"Snapshot {snapshot_id} deleted successfully!")
    except Exception as e:
        print(f"Error deleting snapshot {snapshot_id}: {e}")