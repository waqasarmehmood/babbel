# Overview

This project is a proposed solution to implement a Data Lake by consuming realtime events from a streaming source and creating data lake for analytical usecases.

## Components
There are 3 main components of this repository

* Terraform based IaC project
* Python codebase 
* Documentation

Architectural documents are provided in /docs directory. 

## Prerequisites

Following prerequisites are required to build, test and deploy this project. 

* Docker
* Local Stack
* Terraform
* Python 3.0
* Poetry

## Project Structure

### Terraform 


## How to run?
A make file is provided to build, test and deploy this project in Local Stack. 

## How would you handle duplicate events?
As each event have event_uuid denoting unique idetifier of the event. We can deduplicate on two levels. 

1. Deduplicate in KinesisStreamProcessor by using WaterMark and dropping duplicates on it. 
2. Drop duplicate in Staging layer (Static data)

First step will be used to drop duplicates by keeping track of last n RDDs by keeping this data in spark but this might have performance panelty if we increase watermark duration. 

Staging job should be able to process data incrementally and dropping duplicates in more scalable way. 

## How would you partition the data to ensure good querying performance and scalability?

Given the size of the data 1M events/hour, I decided to partition data on date and event type. This will help transformation in Staging layer by processing data incrementally and by creating pipelines to consume only relevant events by event_type. Staging layer will store data in parquet format and will provide better query execution performance by pushing filters on storage layer. 

## How would you test the different components of your proposed architecture?

Datalake is implemented in layered manner which enables testing different layers independently. Python codebase is divided into independent modules and unit test will help test them locally. 

## How would you ensure the architecture deployed can be replicable across environments?
I have implemented a module based infra setup to ensure services are provisioned according to environment by using environment specific configurations. Modules are generic and will be used to deploy services across environments. 

## Would your proposed solution still be the same if the amount of events is 1000 times smaller or bigger? 
Current architecture is scalable to process 1000 times workload without any issue. Data is partitioned accordingly to enable usecase specific transformation jobs in Staging layer. 

## Would your proposed solution still be the same if adding fields / transforming the data is no longer needed?
We can consider using kinesis firehose to dump this data directly on s3 if transformations are not needed given that firehose would require lambda function to transform data. But, firehose won't provide flexibility to transform, partition, deduplicate and store data in different formats if required in future. I would prefer using Spark Streaming jobs to implement this usecase event if we don't have transformation needs. 
