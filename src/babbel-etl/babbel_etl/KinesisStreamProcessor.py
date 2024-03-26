import sys
from awsglue.transforms import *
from pyspark.context import SparkContext
from pyspark.sql import SparkSession 
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import DataFrame
import pyspark.sql.functions as f
from pyspark.sql.types import *

class KinesisStreamProcessor:

    def __init__(self, kinesis_options: dict, s3_destination_path: str):

        if kinesis_options is None or s3_destination_path is None:
            raise ValueError('Arguments are mandatory.')
        
        if 'streamARN' not in kinesis_options:
            raise ValueError('Kinesis Stream ARN is required.')

        self.name = "KinesisStreamProcessor"
        self.kinesis_options = kinesis_options
        self.s3_destination_path = s3_destination_path

    def __get_stream_schema(self):

        # TODO read schema from schema registry
        return StructType([
            StructField('event_uuid', StringType(), nullable=True),
            StructField('event_name', StringType(), nullable=True),
            StructField('created_at', LongType(), nullable=True),
            StructField('payload', StringType(), nullable=True)
            ])

    def __process_data(self, df:DataFrame, batch_id=None):

        print('batchId: '+str(batch_id)+' count: '+str(df.count()))
        
        batch_df:DataFrame =  df.withColumn("message", f.from_json(f.col('`$json$data_infer_schema$.temporary$`'), self.__get_stream_schema())) \
            .select(f.col('message.*'))
        
        parsed_df = batch_df \
            .withColumn('created_datetime', f.from_unixtime(f.col('created_at'))) \
            .withColumn('event_type', f.split(f.col('event_name'), ':')[0]) \
            .withColumn('event_subtype', f.split(f.col('event_name'), ':')[1]) \
            .withColumn('partition_date', f.to_date(f.col('created_datetime')))
            
        partition_cols = ['partition_date', 'event_type', 'event_subtype']
        parsed_df.write.partitionBy(*partition_cols).mode("append").parquet(f"{self.s3_destination_path}/kinesis_events_data")

    def process(self):

        sc = SparkContext()
        glueContext = GlueContext(sc)
        spark = glueContext.spark_session
        
        job = Job(glueContext)
        job.init(self.name)
        
        streaming_frame = glueContext.create_data_frame.from_options(connection_type="kinesis", connection_options=self.kinesis_options)
        
        glueContext.forEachBatch(frame=streaming_frame,
            batch_function=self.process_data,
            options={
                "windowSize": "30 seconds",
                "checkpointLocation": f"{self.s3_destination_path}/kinesis_events_checkpoint"
            }
        )    
        
        job.commit()
