from pydantic import BaseModel, Field


class RunExperimentBody(BaseModel):
    modelname: str = Field(..., description="DEPENDENCY|PREDICT")
    modeltag: str = Field(..., description="Tag")
    experiment_id: str = Field(..., description="Id")
    stage: str = Field(..., description="STAGING|PRODUCTION")
    requirements_file: str = Field(None, description="STAGING|PRODUCTION")
    model_pkl_file: str = Field(None, description="STAGING|PRODUCTION")


class ExperimentBody(BaseModel):
    experiment_name: str = Field(..., description="Id")
    experiment_tags: dict = Field(..., description="Tags")
    requirements_file: str = Field(..., description="STAGING|PRODUCTION")
    model_pkl_file: str = Field(..., description="STAGING|PRODUCTION")
