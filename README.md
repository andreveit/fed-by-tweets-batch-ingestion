# **Fed By Tweets - Batch Ingestion**


# The Fed By Tweets Project
 
This repository is part of the fedbytweets project. 

The aim of the project is to set up an end-to-end ML system using the AWS infrastructure to ingest, process and extract insights from Twitter data. An NLP model is trained for sentiment analysis and then used to classify the tweets. The final results should be displayed on a dashboard in a public gataway.

The architecture is designed to be primarily covered by the AWS Free Tier, but still be scalable at some degree. The best practices of Data Engineering and MLOps are applied to build the system.


<br>

*This is an ongoing project

---


<br>

# Batch Ingestion

This repository should contain the necessary code to setup the tweets ingestion and processing all the way to the silver layer.


<br>

# Table of Contents
1. [Artchitecture](#Artchitecture)
2. [Data-Lake](#Data-Lake)
3. [Workflow](#Workflow)


<br>

# Artchitecture




 The data is pulled from Twitter's Recent API using the [av-tweet-ingestion](https://github.com/andreveit/av-tweet-ingestion) package, running on a Lambda Function. 
 
 At first, the ideia was to work with AirFlow to orchestrate the jobs, but AWS Step Functions 
happend to be more suitable to the problem, offering better economic advantages besides a handier setup.

For the data processing itself, different tools were evaluated, such as AWS EMR and AWS Glue Jobs.
Lambda Functions ended up being the way to go, as the costs are low and the designed work load wasn't huge. It is also possible to parallelize the processing if necessary.

The tables matadata are kept in the AWS Glue Data Catalog, being possible to query the data and run some analytics using AWS Athena.

The job runs at 7h, 14h and 21h (Brazillian time) and was scheduled through a AWS EventBridge Rule. 

The code to run in the Lambda Functions is containerized (used Docker), making it easy to perform unit tests, integrations tests and setup CI/CD workflows. The CI/CD pipeline was bult with GitHub Actions and Terraform.

Two deployment environments were created, staging and production, as the jobs are running since June/2022 and some updates to the code and the infrastructure were needed.

<br>

![Ingestion architecture](./misc/full_architecture.PNG "Ingestion architecture")


<br>


# Data-Lake

The Data Lake was built with three layers, BRONZE, SILVER and GOLD. The ingested data gets to the BRONZE layer at a designed partition for raw files, in this case json. It is then processed just enough to be read in a tabular format (parquet).The data is modeled in three tables, here we have the TWEETS fact table and two dimensional tables, USERS and PLACES. Up to this point, the data is still kept in the BRONZE layer, even though in a tabular format. At each ingestion, new tweets data are appended to these tables. 

A new ETL process is responsible for taking the data to the SILVER layer. It performs data cleasing, adjusting data types, removing duplicated records and assuring the next layer's data to be trusted.


<br>

Below, it can be seen the schema of each table through the data lake layers.

<br>

![Batch workflow - Step Functions](misc/bronze_schema.PNG "Batch workflow - Step Functions")

<br>

![Batch workflow - Step Functions](misc/silver_schema.PNG "Batch workflow - Step Functions")

<br>



# Workflow

AWS Step Functions is used to orchestrate the data processing through 5 Lambda Functions. 

**Get-Tweets:**
> Hits the Twitter's API and performs the data ingestion.

**Porcessing-Raw:**
> ETL from raw json files to tabular.

**Tweets-to-Silver:**
> ETL Tweets tables from bronze to silver.

**Users-to-Silver:**
> ETL Users tables from bronze to silver.

**Places-to-Silver:**
> ETL Places tables from bronze to silver.


<br>

![Batch workflow - Step Functions](misc/batch-architecture.PNG "Batch workflow - Step Functions")


<br>