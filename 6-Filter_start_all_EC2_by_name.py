#make a list of all ec2 instances as per the name tag given in the filter tag and
# then do start ,stop and terminate action on all instances in bulk
import boto3
aws_mag_con=boto3.session.Session()
ec2_con_cli=aws_mag_con.client("ec2")

np_serv_id=[]

f1={
    "Name" : "tag:Name",
    "Values" :  ["docker server"]
}
response=ec2_con_cli.describe_instances(Filters=[f1])
for each_in in (response["Reservations"]):
    for each_item in each_in["Instances"]:
        print(each_item["InstanceId"])
        print("\n")
        np_serv_id.append(each_item['InstanceId'])
print("list of all instance id are --")
print(np_serv_id)    
print("starting ec2 instances")
ec2_con_cli.start_instances(InstanceIds=np_serv_id)
waiter=ec2_con_cli.get_waiter('instance_running')
waiter.wait(InstanceIds=np_serv_id)  
print("started ec2 instances")
#ec2_con_cli.start_instances(InstanceIds=np_serv_id)    

