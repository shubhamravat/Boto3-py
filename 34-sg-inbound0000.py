import boto3
sg_id_list=[]
aws_mag_con=boto3.session.Session()
ec2_con_cli=aws_mag_con.client("ec2",region_name="us-east-1")
response=ec2_con_cli.describe_security_groups()['SecurityGroups']

for each_item in response:
    #print("Security Group ID: {}".format(each_item['GroupId']))
    group_id_new=each_item['GroupId']
    for permission in each_item['IpPermissions']:
        protocol = permission['IpProtocol']
        #port_range = "{}-{}".format(permission.get('FromPort', nonr), permission.get('ToPort', 'N/A'))
        from_port=permission.get('FromPort', 0)
        to_port=permission.get('ToPort', 65535)
        for i, ip_range in enumerate(permission['IpRanges']):
            if ip_range['CidrIp']=='0.0.0.0/0':
                ip_range_new=ip_range["CidrIp"]
                response = ec2_con_cli.revoke_security_group_ingress(CidrIp=ip_range_new,GroupId=group_id_new,IpProtocol=protocol,ToPort=to_port,FromPort=from_port)
                print('security group {} having 0.0.0.0 inbound rule which is revoked'.format(group_id_new))
            else:
                print("security group {} having no 0.0.0.0 inbound".format(group_id_new))
            #print("Inbound Rule, Source IP: {}".format(ip_range['CidrIp']))
    sg_id_list.append(each_item['GroupId'])

print(sg_id_list)

