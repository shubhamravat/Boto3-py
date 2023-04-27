import boto3
import datetime
import pytz
import datetime
aws_mag_con=boto3.session.Session()
sns_con_cli = aws_mag_con.client("sns")
tz = pytz.timezone('Asia/Kolkata') 
today = datetime.datetime.now().date()
date_today = today.strftime('%Y-%m-%d')
print(date_today)
aws_mag_con=boto3.session.Session()
aws_acm_cli=aws_mag_con.client("acm")
acm_arn_list=[]
sns_topic_arn ="arn:aws:sns:ap-south-1:532102821576:Offer"
response_new = aws_acm_cli.list_certificates(
    CertificateStatuses=[
        'ISSUED'
    ])
#response=aws_acm_cli.describe_certificate(CertificateArn='arn:aws:acm:ap-south-1:532102821576:certificate/75e9b964-f999-4ab7-a59e-fbf0ee063119')
#print(response_new)
for item in response_new['CertificateSummaryList']:
    acm_arn_list.append(item['CertificateArn'])
    print(item)
    res=item['NotAfter']
    print(res,"normal format from AWS end")
    #date_str = res.strftime('%Y-%m-%d')
    #print(date_str,"after strftime of above format")
    

    #date_str = '2024-03-21'
    #date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    #print(date_obj,"strptime of above format")
    exp_date = res - datetime.timedelta(days=395)
    exp_date_str = exp_date.strftime('%Y-%m-%d')
    print(exp_date_str)
    if date_today==exp_date_str:
        message = f"The certificate with domain name= {item['DomainName']} and arn = {item['CertificateArn']} going to expire today."
        response = sns_con_cli.publish(TopicArn=sns_topic_arn, Message=message)
        print("SNS message sent:", response['MessageId'])
    else:
         print("time not matching")

print(acm_arn_list)