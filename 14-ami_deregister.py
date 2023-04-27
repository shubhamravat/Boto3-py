import boto3
import datetime
import pytz
from datetime import datetime
aws_mag_con=boto3.session.Session()
aws_ec2_cli=aws_mag_con.client("ec2")
tz = pytz.timezone('Asia/Kolkata') 
now = datetime.now(tz)
ami_list=[]
ami_list_new=[]
response=aws_ec2_cli.describe_images(Owners=["532102821576"])
for item in response['Images']:
    ami_list.append(item['ImageId'])
    print(item['CreationDate'])
    date_obj = datetime.fromisoformat(item['CreationDate'])
    print(date_obj)
    new_date_str = date_obj.strftime("%y-%m-%d")
    if new_date_str>='23-02-16':
        ami_list_new.append(item['ImageId'])
        #aws_ec2_cli.deregister_image(ImageId=item['ImageId'])
        #print("deregistering the image {}".format(item['ImageId']))
print("no ami found")           
print(ami_list)
print(ami_list_new)
