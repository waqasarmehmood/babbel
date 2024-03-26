import sys
from awsglue.utils import getResolvedOptions
from babbel_etl import KinesisStreamProcessor

if __name__ == "__main__":
    
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])

    # reference for stream
    # https://docs.aws.amazon.com/kinesis/latest/APIReference/API_StartingPosition.html
    # TRIM_HORIZON  | LATEST

    kinesis_options = { 
        "streamARN": args["STREAM_ARN"],
        "startingPosition": "TRIM_HORIZON", 
        "inferSchema": "true", 
        "classification": "json",
        "awsSTSRoleARN": args["CROSS_ACCOUNT_ASSUME_ROLE"],
        "awsSTSSessionName": "optional-session"
    }

    s3_destination_path = args["S3_DESTINATION_PATH"]

    stream_processor = KinesisStreamProcessor(kinesis_options, s3_destination_path)
    stream_processor.process()