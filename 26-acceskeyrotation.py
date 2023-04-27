###strptime for adding
###strftime for comparing date

import boto3
import datetime
import pytz
import datetime
aws_mag_con=boto3.session.Session()
sns_con_cli = aws_mag_con.client("sns")
tz = pytz.timezone('Asia/Kolkata') 
today = datetime.datetime.now().date()
date_today = today.strftime('%Y-%m-%d')
print(f"todays date is {date_today}\n")
aws_mag_con=boto3.session.Session()
aws_iam_cli=aws_mag_con.client('iam')
response=aws_iam_cli.list_users()['Users']
sns_topic_arn ="arn:aws:sns:ap-south-1:532102821576:Offer"
iam_name_list=[]

for item in response:
    iam_name_list.append(item['UserName'])
for iam_user in iam_name_list:
    iam_user_each=aws_iam_cli.list_access_keys(UserName=iam_user)
    #first_access_key=None
    #second_access_key=None
#print(iam_user_each)
    try:
        first_access_key=iam_user_each['AccessKeyMetadata'][0]['AccessKeyId']
        first_access_key_creation_date=iam_user_each['AccessKeyMetadata'][0]['CreateDate'].strftime('%Y-%m-%d')
        first_access_key_creation_date = datetime.datetime.strptime(first_access_key_creation_date, '%Y-%m-%d')
        exp_date_first_key = first_access_key_creation_date + datetime.timedelta(days=5)
        exp_date_first_key=exp_date_first_key.strftime('%Y-%m-%d')
        print("creation date of first key final is",first_access_key_creation_date)
        print("\nexp date of first key is",exp_date_first_key)
        if date_today==exp_date_first_key:
            print(f"\naccess key expired is {first_access_key}\n")
            response_access_key_update_first=aws_iam_cli.update_access_key(AccessKeyId=first_access_key,
Status='Active',
    UserName=iam_user,
)
            #print(response_access_key_update_first)
            response_access_key_new_first = aws_iam_cli.create_access_key(
    UserName=iam_user
)
            new_first_access_key=response_access_key_new_first['AccessKey']['AccessKeyId']
            new_first_secret_key=response_access_key_new_first['AccessKey']["SecretAccessKey"]
            print("\nnew access key",new_first_access_key)
            print("\nnew secret key",new_first_secret_key)
            message = f"Access key id {first_access_key} is expired , new access key is {new_first_access_key} and its secret access key is {new_first_secret_key}"
            response = sns_con_cli.publish(TopicArn=sns_topic_arn, Message=message)
            print("SNS message sent:", response['MessageId'])
#print(response_access_key_new)


        else:
            print("\nexpiry date and creation date not matchced")
    except:
        print(f"\nfirst access key of user {iam_user} = {first_access_key} and second access key of user {iam_user} = NA") 

    try:    
        second_access_key=iam_user_each['AccessKeyMetadata'][1]['AccessKeyId']
        second_access_key_creation_date=iam_user_each['AccessKeyMetadata'][1]['CreateDate'].strftime('%Y-%m-%d')
        second_access_key_creation_date = datetime.datetime.strptime(second_access_key_creation_date, '%Y-%m-%d')
        exp_date_second_key = second_access_key_creation_date + datetime.timedelta(days=19)
        exp_date_second_key=exp_date_second_key.strftime('%Y-%m-%d')
        print("\ncreation date of second key final is",second_access_key_creation_date)
        print("\nexp date of first key is",exp_date_second_key)
        if date_today==exp_date_second_key:
            print(f"\nkey expired is {second_access_key}")
            response_access_key_update_second=aws_iam_cli.update_access_key(AccessKeyId=second_access_key,
Status='Active',
    UserName=iam_user,
)   
            response_access_key_new_second = aws_iam_cli.create_access_key(
    UserName=iam_user

)       
            new_second_access_key=response_access_key_new_second['AccessKey'][1]['AccessKeyId']
            new_second_secret_key=response_access_key_new_second['AccessKey'][1]["SecretAccessKey"]
            print("\nnew access key",new_second_access_key)
            print("\nnew secret key",new_second_secret_key)
            message = f"Access key id {second_access_key} is expired , new access key is {new_second_access_key} and its secret access key is {new_second_secret_key}"
            response = sns_con_cli.publish(TopicArn=sns_topic_arn, Message=message)
            print("SNS message sent:", response['MessageId'])
        
        else:
            print("\nexpiry date and creation date not matchced")
            print(f"\nfirst access key of user {iam_user} = {first_access_key} with creation date ={first_access_key_creation_date} and second access key of user {iam_user} ={second_access_key} with creation date ={second_access_key_creation_date}")
        
    except:
        print(f"\nfirst access key of user {iam_user} = {first_access_key} and second access key of user {iam_user} = NA") 

    
print("\n",iam_name_list)    

'''
for iam_user in iam_name_list:
    iam_user_each=aws_iam_cli.list_access_keys(UserName=iam_user)
    #print(iam_user_each)
    try:
        first_access_key=iam_user_each['AccessKeyMetadata'][0]['AccessKeyId']
        second_access_key=iam_user_each['AccessKeyMetadata'][1]['AccessKeyId'] 
        print(f"first access key of user {iam_user} = {first_access_key} and second access key of user {iam_user} ={second_access_key}")
    except:
        print(f"first access key of user {iam_user} = {first_access_key} and second access key of user {iam_user} = NA") 

    #print(iam_user_each)

#response_access_key_update=aws_iam_cli.update_access_key(AccessKeyId='AKIAXXY6MW3EG2PVCIMH',
#    Status='Active',
#    UserName='Boto3-test',
#)

#response_access_key_new = aws_iam_cli.create_access_key(
#    UserName='Boto3-test'
#)
#print(response_access_key_new)
    '''