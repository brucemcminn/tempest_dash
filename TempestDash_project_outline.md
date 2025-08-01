# AWS Data Ingestion Pipeline for Weather Data

## AWS Account & Security Setup
- [x] Created AWS account
- [x] Set up root and IAM user
- [x] Created **Customer Managed KMS key** for encryption
  - [x] Verified cost model and enabled key rotation
  - [x] Updated KMS policy to allow access for Glue and IAM users
- [x] Created **S3 bucket** for raw and historical data
- [x] Managed IAM roles and permissions for Glue crawler
- [ ] (Optional) Created **programmatic keys** for CLI or SDK access

## Development & Source Control
- [x] Initialized Git repo for pipeline project
- [x] Connected Git repo to **Visual Studio Code**
- [x] Developed in **virtual environment** with versioned dependencies

## Python Scripting & Data Collection
- [x] Wrote Python script to call **Tempest API** for historical weather data
  - [x] Stored API keys securely via `.env` and `dotenv`
  - [x] Chunked large time ranges into valid epochs
- [x] Saved resulting data to:
  - [x] Local CSV files
  - [x] **Uploaded to S3** using `boto3`

## AWS Glue Integration
- [x] Created **custom Glue crawler**
  - [x] Scoped to proper S3 prefix
  - [x] Used **custom classifier** to handle CSV quirks
- [x] Updated KMS policy to allow Glue's service role to decrypt files
- [x] Inferred schema and created **Data Catalog table**
- [x] Diagnosed and resolved:
  - [x] Inference failure from malformed CSVs
  - [x] Permission errors (S3 and KMS)
  - [x] Classification failures due to trailing commas

## Next Steps
- [ ] Implement **automated preprocessing pipeline**
  - [ ] Trigger: S3 Event
  - [ ] Transform: AWS Lambda (removes trailing commas)
  - [ ] Output: Cleaned files into a `cleaned/` prefix
  - [ ] Re-crawl with Glue
- [ ] Add support for **"current conditions"** or rolling 5–10 day window
- [ ] (Optional) Store raw + cleaned data in separate buckets or partitions

## Optional Enhancements (Portfolio Polish)
- [ ] Schedule daily Lambda/API calls using **CloudWatch Events**
- [ ] Use **AWS Glue Job** for scalable PySpark data processing
- [ ] Visualize results in Power BI / QuickSight
- [ ] Document pipeline architecture in README or diagram (PlantUML or Draw.io)