import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME
from google.cloud import storage
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR

from dotenv import load_dotenv


from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        
        load_dotenv()

        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        self.client = storage.Client()

    def start_data_ingestion(self):
        try:
            self.data_intestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info('Start data Ingestion')
            data_ingestion=DataIngestion(data_ingestion_config=self.data_intestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f'Data Ingestion completed and artifact: {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        
        try:
            data_validation_config=DataValidationConfig(trainig_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info('Initiate teh data Validation')
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) ->ModelTrainerArtifact:
        try:
            self.start_model_trainer_config:ModelTrainerConfig= ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.start_model_trainer_config
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## local artifact is going to s3 bucket    
    def sync_artifact_dir_to_gcs(self):
        try:
            gcs_bucket_url = f"gs://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            
            self.sync_folder_to_gcs(
                folder=self.training_pipeline_config.artifact_dir,
                gcs_bucket_url=gcs_bucket_url
            )
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## local final model is going to s3 bucket 
        
    def sync_saved_model_dir_to_gcs(self):
        try:
            gcs_bucket_url = f"gs://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            
            self.sync_folder_to_gcs(
                folder=self.training_pipeline_config.model_dir,
                gcs_bucket_url=gcs_bucket_url
            )
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def sync_folder_to_gcs(self,folder, gcs_bucket_url):
        bucket_name= gcs_bucket_url.split('/')[2]
        blob_path = '/'.join(gcs_bucket_url.split('/')[3:])

        bucket = self.client.get_bucket(bucket_name)
        for root, dirs, files in os.walk(folder):
            for file in files:
                local_file = os.path.join(root, file)
                blob = bucket.blob(os.path.join(blob_path, os.path.relpath(local_file, folder)))
                blob.upload_from_filename(local_file)

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)

            self.sync_artifact_dir_to_gcs()
            self.sync_saved_model_dir_to_gcs()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)