
import boto3
import os
import tempfile

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Parse the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    target_bucket = source_bucket  # Writing to same bucket
    target_key = source_key.replace("raw/", "clean/")

    # Download the raw file
    with tempfile.NamedTemporaryFile() as tmp_in, tempfile.NamedTemporaryFile() as tmp_out:
        s3.download_file(source_bucket, source_key, tmp_in.name)

        with open(tmp_in.name, 'r') as infile, open(tmp_out.name, 'w') as outfile:
            for line in infile:
                cleaned = line.rstrip().rstrip(',') + '\n'
                outfile.write(cleaned)

        # Upload the cleaned file
        s3.upload_file(tmp_out.name, target_bucket, target_key)

    return {
        'statusCode': 200,
        'body': f'Cleaned file written to s3://{target_bucket}/{target_key}'
    }
