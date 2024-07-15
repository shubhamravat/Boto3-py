import boto3
from twilio.rest import Client
import time
from datetime import datetime ,timedelta
from twilio.twiml.voice_response import Play, VoiceResponse
import subprocess
from io import BytesIO
from dateutil import tz


# EXTRACT THE ALERT NAME CONVERT THE NAME INTO TXT FILE AND STORE ALERT NAME AS CONTENT INTO TXT FILE - THEN USE ALERT NAME
# AND CONVERT IT INTO MP3 AUDIO - 
s3 = boto3.client('s3')

def alert_count_check(alert_name):
    window_minutes=10
    ist_timezone = tz.gettz('Asia/Kolkata')
    
    # Get the current time in IST
    current_time_ist_aware = datetime.now(ist_timezone)
    
    # Calculate the start time for the window (10 minutes ago) in IST
    window_start_time_ist_aware = current_time_ist_aware - timedelta(minutes=10)
    
    
    #alert_name_body="P1 Alert-MSP-AWS/EC2-i-049e947070b098f5f/EC2-4-fourth-instance-StatusCheckFailed"
    modified_alert_name_incount = alert_name.replace('/', '_')
    prefix = f'{modified_alert_name_incount}_'
    print("THIs IS PREFIX",prefix)
    current_time = datetime.utcnow()
    window_start_time = current_time - timedelta(minutes=window_minutes)
    print(current_time)
    print(window_start_time)
    objects = s3.list_objects(Bucket='software-ssm', Prefix=prefix)
    print(objects)
    recent_alerts = [
        obj['Key'] 
        for obj in objects.get('Contents', []) 
        if obj['LastModified'] >= window_start_time_ist_aware
    ]
    print(recent_alerts)
    print(len(recent_alerts))
    return(len(recent_alerts))
        
    

def upload_txt_to_s3(alert_name , bucket_name_txt,alert_name_body):
    try:
        modified_alert_name = alert_name.replace('/', '_')
        final_txt_name=f'{modified_alert_name}_{datetime.utcnow()}.txt'
        print(final_txt_name)
        s3.put_object(Body=alert_name_body, Bucket='software-ssm', Key=final_txt_name)
    except Exception as e:
        print("issue with upload txt to s3 function")
        #raise
    return alert_name_body
    

def convert_to_pcm_mulaw(input_bytes):
    try:
        # Use ffmpeg to convert MP3 to PCM mu-law
        result = subprocess.run(["ffmpeg", "-i", "pipe:0", "-f", "wav", "-acodec", "pcm_mulaw", "-ar", "8000", "-ac", "1", "pipe:1"], input=input_bytes, stdout=subprocess.PIPE)
        return result.stdout
    except Exception as e:
        print(f"Error in convert_to_pcm_mulaw: {e}")
        return None

def generate_audio_from_text(text, output_format='mp3', voice_id='Aditi'):
    polly_client = boto3.client('polly')
    
    response = polly_client.synthesize_speech(
        Text=text,
        Engine='standard',
        OutputFormat=output_format,
        VoiceId=voice_id,
        SampleRate='8000',
        LanguageCode='en-IN',
    )

    # Convert MP3 to PCM mu-law
    pcm_mulaw_bytes = convert_to_pcm_mulaw(response['AudioStream'].read())

    # Save the mu-law audio to an S3 bucket
    #s3 = boto3.client('s3')
    #phone_audio_key = f'{int(time.time())}.mp3'
    phone_audio_key = f'{text}.mp3'
    
    s3.put_object(Body=pcm_mulaw_bytes, Bucket='phone-call-alert-bucket', Key=phone_audio_key)
    pre_signed_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'phone-call-alert-bucket', 'Key': phone_audio_key},
        ExpiresIn=720)
    
    print(pre_signed_url)

    # Return the pre-signed URL
    return pre_signed_url
    # Return the URL of the generated audio file
    #return f'https://phone-call-alert-bucket.s3.ap-south-1.amazonaws.com/{phone_audio_key}'

def lambda_handler(event, context):

    print("Lambda function started.")
    
    bucket_name = 'phone-call-alert-bucket'
    bucket_name_txt='software-ssm'
    
    aud_var = "Hi, you have received a P1 alert ALert name is "
    #alert_name_body=f"{aud_var}P1 Alert-MSP-AWS/EC2-i-049e947070b098f5f/EC2-4-fourth-instance-StatusCheckFailed"
    alert_name_body="Hi, This is to let You know that you have received more than 4 alarms in last 5 minutes. kindly take appropriate action"
    alert_name = "P1 Alert-MSP-AWS/EC2-i-049e947070b098f5f/EC2-4-fourth-instance-StatusCheckFailed"
    #modified_alert_name_txt = alert_name_txt.replace('/', '_')
    #s3.put_object(Body=alert_name, Bucket='software-ssm', Key=f'{modified_alert_name_txt}_{datetime.utcnow()}.txt')
    upload_txt_to_s3_return_value=  upload_txt_to_s3(alert_name , bucket_name_txt,alert_name_body)
    print(upload_txt_to_s3_return_value)
    alert_count_check_return_value=alert_count_check(alert_name)
    print(alert_count_check_return_value)
    if alert_count_check_return_value >= 1:
        audio_url = generate_audio_from_text(upload_txt_to_s3_return_value)
        final_phone_call(audio_url)
    else:
        print("cant call")
    
    print(upload_txt_to_s3_return_value)
    #print(audio_url)                                    

def final_phone_call(audio_url):
    
    account_sid = "xxxxxxxxx"
    auth_token = 'xxxxxxxxxxxxxxx'
    client = Client(account_sid, auth_token)

    # Create TwiML response to play the audio file
    response = VoiceResponse()
    response.play(audio_url)

    # Create a call and include the TwiML response
    call = client.calls.create(
        to='+918077959813',
        from_='+918077959813',
        twiml=str(response)
    )

    print(call.sid)

    print("Lambda function completed successfully.")





'''
import boto3
from twilio.rest import Client
import time
from twilio.twiml.voice_response import Play, VoiceResponse
import subprocess

def convert_to_wav(input_path, output_path):
    try:
        # Use ffmpeg to convert MP3 to WAV
        subprocess.run(["ffmpeg", "-i", input_path, "-ac", "1", output_path])
    except Exception as e:
        print(f"Error in convert_to_wav: {e}")

def convert_to_pcm_mulaw(input_path, output_path):
    try:
        # Use ffmpeg to convert WAV to PCM mu-law
        subprocess.run(["ffmpeg", "-i", input_path, "-acodec", "pcm_mulaw", "-ar", "8000", "-ac", "1", output_path])
    except Exception as e:
        print(f"Error in convert_to_pcm_mulaw: {e}")

def generate_audio_from_text(text, output_format='mp3', voice_id='Joanna'):
    polly_client = boto3.client('polly')
    
    response = polly_client.synthesize_speech(
        Text=text,
        Engine='standard',
        OutputFormat=output_format,
        VoiceId=voice_id,
        SampleRate='8000',
        LanguageCode='en-IN',
    )

    # Save the original audio to an S3 bucket
    s3 = boto3.client('s3')
    original_audio_key = f'{int(time.time())}.{output_format}'
    converted_audio_key = f'{int(time.time())}.wav'  # Set the desired extension, e.g., '.wav'

    s3.put_object(Body=response['AudioStream'].read(), Bucket='guess-the-number-khel', Key=original_audio_key)

    # Download the original file from S3
    local_path = '/tmp/original_audio.mp3'
    s3.download_file("guess-the-number-khel", original_audio_key, local_path)

    # Convert format to WAV using FFmpeg
    converted_audio_path = '/tmp/converted_audio.wav'
    convert_to_wav(local_path, converted_audio_path)

    # Convert WAV to PCM mu-law using FFmpeg
    phone_audio_path = '/tmp/phone_audio.wav'
    convert_to_pcm_mulaw(converted_audio_path, phone_audio_path)

    # Upload the converted file back to S3 with the same key
    s3.upload_file(phone_audio_path, 'guess-the-number-khel', converted_audio_key)

    # Return the URL of the generated audio file
    return f'https://guess-the-number-khel.s3.ap-south-1.amazonaws.com/{converted_audio_key}'

def lambda_handler(event, context):
    print("Lambda function started.")

    # Replace these values with your S3 bucket name and key
    bucket_name = 'guess-the-number-khel'

    # Replace this with your alert name logic
    aud_var = "Hi, you have received a P1 alert."
    alert_name = f"{aud_var}P1 Alert-MSP-AWS/EC2-i-049e947070b098f5f/EC2-4-fourth-instance-StatusCheckFailed"
    audio_url = generate_audio_from_text(alert_name)
    print(audio_url)

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = "AC810b39834c84ad345f3d23cba50f132b"
    auth_token = 'c574245bce1e520751c394715e05ff28'
    client = Client(account_sid, auth_token)

    # Create TwiML response to play the audio file
    response = VoiceResponse()
    response.play(audio_url)
    #response.play(audio_url, loop=1).audio_codec('audio/wav')

    # Create a call and include the TwiML response
    call = client.calls.create(
        to='+918077959813',
        from_='+918077959813',
        twiml=str(response)
    )

    print(call.sid)

    print("Lambda function completed successfully.")





'''
