import boto3
aws_mag_console=boto3.session.Session()
sts_con_cli=aws_mag_console.client("sts")
response=sts_con_cli.get_caller_identity()
print(response["Account"])
