import boto3
import boto3
aws_mag_con=boto3.session.Session()
sns_con_cli = aws_mag_con.client("ses")
#sns_topic_arn ="arn:aws:sns:ap-south-1:532102821576:Offer"
