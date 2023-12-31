import os, sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.utils import save_obj

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocess_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation(self):
        try:
            numerical_features = ['reading_score','writing_score']
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            num_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Numerical columns: {numerical_features}")
            logging.info(f"Categorical columns: {categorical_features}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("categorical_pipeline", categorical_pipeline, categorical_features)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Start reading data from training and testing directory")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            preprocessing_obj = self.get_data_transformation()
            target_column = 'math_score'

            input_feature_train_df = train_df.drop(columns=[target_column], axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column], axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info('Applying preprocessing on training and test data')
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info('Saved preprocessing object')

            save_obj(
                file_path = self.data_transformation_config.preprocess_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocess_obj_file_path
            )



        except Exception as e:
            raise CustomException(e, sys)
