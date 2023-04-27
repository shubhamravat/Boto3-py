import boto3
aws_mag_con=boto3.session.Session()
ec2_con_cli=aws_mag_con.client("ec2")
ebs_unused_list=[]
response=ec2_con_cli.describe_volumes()['Volumes']
for each_in in response:
    if each_in['State']=='available':
        ebs_unused_list.append(each_in['VolumeId'])
        ec2_con_cli.delete_volume(VolumeId=each_in['VolumeId'])
        print("deleting volume id {} UNUSED".format(each_in['VolumeId']))
        
        

print("list of all volume id UNUSED :{}".format(ebs_unused_list))
#ec2_con_cli.delete_volume(VolumeId=ebs_unused_list)


