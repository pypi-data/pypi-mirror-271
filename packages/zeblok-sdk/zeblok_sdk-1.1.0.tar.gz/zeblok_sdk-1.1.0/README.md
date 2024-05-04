# Zeblok Python SDK

Zeblok-sdk will help integrate your MLOps workflows with the Zeblok Ai-MicroCloud platform.

## Components of the Python SDK

### Auth

- API Authentication
- Datalake Authentication

### Resources

- Plan
- Namespace

### Managed Service

- Microservice
- Orchestration-Addons
- Ai-API
- Ai-Pipeline
- DataSet

# Interface

<h3> Authentication </h3>

- API Authentication: `APIAuth(app_url, api_access_key,api_access_secret)`
- Datalake Authentication: `DataSet(api_auth, access_key, secret_key, bucket_name)`

<h3> Plans </h3>

- Get all plans: `get_all()`
- Get a plan by id: `get_by_id(plan_id)`
- Validate a plan by id: `validate_id(plan_id)`
- Get filtered details of a plan: `get_filtered_details(plan_id, fields_req)`

<h3> Namespaces </h3>

- Get all namespaces: `get_all()`
- Get a namespace by id: `get_by_id(namespace_id)`
- Validate a namespace by id: `validate_id(namespace_id)`

<h3> MicroServices </h3>

- Get all microservices: `get_all()`
- Get a microservice by id: `get_by_id(plan_id)`
- Validate a microservice by id: `validate_id(microservice_id)`
- Spawn a microservices by
  id: `spawn(display_name, microservice_id, plan_id, microservice_name, namespace_id, envs, ports, args, command)`

<h3> Orchestration-Addons </h3>

- Get all orchestrations: `get_all()`
- Get an orchestration by id: `get_by_id(orchestration_id)`
- Validate an orchestration by id: `validate_id(orchestration_id)`
- Spawn an orchestrations by
  id: `spawn(orchestration_id, plan_id, namespace_id, orchestration_name, min_workers, max_workers)`

<h3> AI-APIs </h3>

- Get all AI-APIs with `deployed` state: `get_all(state=deployed)`
- Get all AI-APIs with `ready` state: `get_all(state=ready)`
- Validate an AI-API: `validate(image_name, state)`
- Create and Spawn an AI-API: `create_and_spawn(ai_api_name, model_folder_path, plan_id, namespace_id, ai_api_type)`
- Create an AI-API: `create(ai_api_name, model_folder_path, ai_api_type)`
- Spawn an AI-API: `spawn(image_name, namespace_id, plan_id)`

<h3> AI-Pipelines </h3>

- Get all AI-Pipelines with `created` state: `get_all(state=created)`
- Get all AI-Pipelines with `ready` state: `get_all(state=ready)`
- Validate an AI-Pipeline: `validate(image_name, state)`
- Create and Spawn an
  AI-API: `create_and_spawn(ai_pipeline_name, ai_pipeline_folder_path, caas_plan_id, ai_pipeline_plan_id, namespace_id)`
- Create an
  AI-Pipeline: `create(ai_pipeline_name, ai_pipeline_folder_path, caas_plan_id, ai_pipeline_plan_id, namespace_id)`
- Spawn an AI-Pipeline: `spawn(ai_pipeline_plan_id, namespace_id, ai_pipeline_image_name)`

<h3> DataSet </h3>

- Check if a bucket exists: `bucket_exists()`
- Check if an object exists: `object_exists(object_name)`
- Upload an object: `upload_object(local_file_pathname, object_name)`
- Download an object: `download_object(object_name, local_dir, filename)`
- Get object PreSigned URL: `get_presigned_url(object_name)`

## Usage

Checkout the detailed usage of the SDK at [Usage.md](Usage.md#usage)

# Contact Zeblok

| **Team**           | **Email**          |
|--------------------|--------------------|
| **Technical Team** | support@zeblok.com |
| **Sales Team**     | sales@zeblok.com   |

