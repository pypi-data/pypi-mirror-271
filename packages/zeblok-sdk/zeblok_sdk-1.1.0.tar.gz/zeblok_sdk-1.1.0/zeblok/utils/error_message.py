# GENERAL

INCOMPATIBLE_SERVICE_PLAN_ID = r'The given plan id ({plan_id}) has a service type `{service_type_1}`. Expected a plan with service type `{service_type_2}`.'
PLAN_ID_TYPE_UNAVAILABLE = r'Could not find the `type` of the plan id ({plan_id}).'
PLAN_ID_DATACENTER_UNAVAILABLE = r'Could not find the `DataCenter` of the plan id ({plan_id}).'

EMPTY_MODEL_FOLDER_PATH = r"model_folder_path is empty"
MODEL_FOLDER_PATH_NOT_DIR = r"{model_folder_path} is not a Directory."
MODEL_FOLDER_PATH_DOES_NOT_EXIST = r"No such Directory ({model_folder_path}) found."
MODEL_FOLDER_PARENT_PATH_NO_WRITE_PERMISSION = r"Directory ({model_folder_path}) does not have write permission."

# API_ACCESS_KEY
INVALID_API_ACCESS_KEY_TYPE = r'API_ACCESS_KEY can only be of type String'
EMPTY_API_ACCESS_KEY = r'API_ACCESS_KEY cannot be empty'

# API_ACCESS_SECRET
INVALID_API_ACCESS_SECRET_TYPE = r'API_ACCESS_SECRET can only be of type String'
EMPTY_API_ACCESS_SECRET = r'API_ACCESS_SECRET cannot be empty'

# DATALAKE_USERNAME
INVALID_DATALAKE_USERNAME_TYPE = r'API_ACCESS_KEY can only be of type String'
EMPTY_DATALAKE_USERNAME = r'API_ACCESS_KEY cannot be empty'

# DATALAKE_SECRET_KEY
INVALID_DATALAKE_SECRET_KEY_TYPE = r'API_ACCESS_SECRET can only be of type String'
EMPTY_DATALAKE_SECRET_KEY = r'API_ACCESS_SECRET cannot be empty'

# BUCKET
INVALID_BUCKET_NAME_TYPE = r"bucket_name can only be of type String"
EMPTY_BUCKET_NAME = r"bucket_name cannot empty"

# NAMESPACE
NO_NAMESPACES = r"No namespaces available in this environment. Please create a namespace."
NO_NAMESPACE_ID = r"No namespace with id ({namespace_id}) in this environment."

# PLAN
NO_PLANS = r"No plans available in this environment. Please create a plan."
NO_PLAN_ID = r"No plan with id ({plan_id}) in this environment."

# MICROSERVICES
NO_MICROSERVICES = r"No microservice available in this environment. Please create a microservice."
NO_MICROSERVICES_ID = r"No microservice with id ({microservice_id}) in this environment."
INVALID_MICROSERVICE_DISPLAY_NAME = r"MicroService (id: {microservice_id}) has no display_name `{display_name}`."

# ORCHESTRATION
NO_ORCHESTRATIONS = r"No orchestrations available in this environment. Please create an orchestration."
NO_ORCHESTRATION_ID = r"No orchestration with id ({orchestration_id}) in this environment."

# AI-PIPELINE
EMPTY_AI_PIPELINE_NAME = r'ai_pipeline_name cannot be empty'
INVALID_AI_PIPELINE_NAME_TYPE = r"ai_pipeline_name can only be of type String"
NO_AI_PIPELINE_STATE = r"No AI-Pipeline available in this environment with {state} state."
NO_AI_PIPELINE_IMAGE_NAME = r"No `created` state AI-Pipeline with image_name ({image_name}) in this environment."

# AI-API
INVALID_AI_API_NAME_TYPE = r"ai_api_type can only be of type String"
EMPTY_AI_API_NAME = r'ai_api_type cannot be empty'
INVALID_AI_API_TYPE_TYPE = r"ai_api_type can only be of type String"
EMPTY_AI_API_TYPE = r'ai_api_type cannot be empty'
INVALID_AI_API_TYPE = r"ai_api_type should be one of 'bentoml', 'openvino', 'mlflow','llm'"
NO_AI_API_STATE = r"No AI-APIs available in this environment with {state} state."
NO_AI_API_IMAGE_NAME = r"No `ready` state AI-API with image_name ({image_name}) in this environment."
