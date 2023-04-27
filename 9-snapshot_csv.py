import boto3
import csv
aws_mag_console=boto3.session.Session()
ec2_con_cli=aws_mag_console.client("ec2")
csv_ob=open("snapshot_inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_No","Snapshot_Id","VolumeId","VolumeSize","State"])
count=1
filt1={
            'Name': 'status',
            'Values': [
                'completed',
            ]
        }

'''filt2={
            'Name': 'volume-size',
            'Values': [
                '8','10'
            ]
        }
'''
response = ec2_con_cli.describe_snapshots(Filters=[filt1],OwnerIds=["532102821576"])   
for each_in in response['Snapshots']:
        print(count,each_in['SnapshotId'],each_in['VolumeId'],each_in['VolumeSize'])
        csv_w.writerow([count,each_in['SnapshotId'],each_in['VolumeId'],each_in['VolumeSize'],each_in['State']])
        count=count+1


csv_ob.close()