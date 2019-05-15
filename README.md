# Sparkify - Data Warehousing with AWS Redshift
With song database and user activity logs residing in directories of JSON files in S3, we built an ETL pipeline.

The pipeline extracts data from S3, stages the data onto Redshift, and transforms the data into dimensional tables for analytics.

## Files
* create_tables.py - connects to Redshift and creates the tables, dropping if any exist
* sql_queries.py - contains the sql queries for all the tables
* dwh.cfg - contains configuration files for AWS (not included in this git repository since they're secret)
* etl.py - loads staging tables and inserts data into dimensional tables to be usable for analytic queries

## Usage
* Fill out dwh.cfg using your IAM role and cluster information
* Initialize your Redshift cluster (using aws-cli, the boto3 python package, or using AWS Cloudformation for infrastructure as Code)
* Create tables using `python create_tables.py`
* Run ETL using `python etl.py`