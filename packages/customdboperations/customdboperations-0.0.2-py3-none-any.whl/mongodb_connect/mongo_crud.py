import pandas as pd
import json
import os
import sys
from pathlib import Path
from ensure import ensure_annotations
from typing import Union
from pymongo.mongo_client import MongoClient # type: ignore

class mongodb:
    
    def __init__(self, client_url: str, database_name: str, collection_name: str):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def __connect_to_db(self) -> MongoClient:
        client: MongoClient = MongoClient(self.client_url)

        try:
            client.admin.command('ping')
            print("Pinged your deployment. You are successfully connected to a MongoDB!")
            return client
        
        except Exception as e:
            raise e
        
    @ensure_annotations
    def __create_database(self, database_name: str):
        client = self.__connect_to_db()
        database = client[database_name]
        print("Database created successfully!")

        return database
    
    @ensure_annotations
    def __create_collection(self, collection_name: str, database_name: str):
        if database_name == None:
            database = self.__create_database(self.database_name)
        else:
            database = self.__create_database(database_name)

        collection = database[collection_name]
        print("Collection created successfully!")

        return collection
    
    @ensure_annotations
    def insert(self, data: Union[dict, list], database_name: str = None,  collection_name: str = None):
        if type(data) == list:
            for record in data:
                if type(record) != dict:    
                    raise TypeError("Each individual record must be in dictionary format...")
                
            if collection_name == None:
                collection = self.__create_collection(self.collection_name, database_name)
            else:
                collection = self.__create_collection(collection_name, database_name)

            collection.insert_many(data)

        elif type(data) == dict:
            if collection_name == None:
                collection = self.__create_collection(self.collection_name, database_name)
            else:
                collection = self.__create_collection(collection_name, database_name)

            collection.insert_one(data)

        print("Data inserted successfully in the collection.")

    @ensure_annotations
    def insert_dataframe(self, data_path: str, database_name: str = None, collection_name: str = None):
        if data_path.endswith(".csv"):
            df = pd.read_csv(data_path, encoding='utf-8')

        elif data_path.endswith(".xlsx"):
            df = pd.read_csv(data_path, encoding='utf-8')

        json_records = list(json.loads(df.T.to_json()).values())

        if collection_name == None:
            collection = self.__create_collection(self.collection_name, database_name)
        else:
            collection = self.__create_collection(collection_name, database_name)

        collection.insert_many(json_records)

        print("Dataframe inserted successfully in the collection.")

    @ensure_annotations
    def __get_size(self, path: Path) -> str:
        """get size in KB

        Args:
            path (Path): path of the file

        Returns:
            str: size in KB
        """
        size_in_kb = round(os.path.getsize(path)/1024)
        return f"~ {size_in_kb} KB"
    
    @ensure_annotations
    def __create_directories(self, path_to_directories: list, verbose=True):
        """create list of directories

        Args:
            path_to_directories (list): list of path of directories
            ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
        """
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                print(f"created directory at: {path}")

    @ensure_annotations
    def __export_collection_as_dataframe(self, database_name: str, collection_name: str) -> pd.DataFrame:
        client = self.__connect_to_db()

        collection = client[database_name][collection_name]

        df = pd.DataFrame(list(collection.find()))

        if '_id' in df.columns.to_list():
            df.drop(columns=['_id'], axis=1, inplace=True)

        return df
    
    @ensure_annotations
    def __export_data_into_file_path(self, database_name: str, collection_name: str, local_data_path: Path, root_dir: str) -> str:

        data = self.__export_collection_as_dataframe(database_name, collection_name)

        self.__create_directories([root_dir])

        if not os.path.exists(local_data_path):
            data.to_csv(local_data_path, index=False)
            return f"exported data from mongoDB stored at {local_data_path}"
        
        else:
            return f"file already exists of size: {self.__get_size(local_data_path)}"

    @ensure_annotations
    def get_data(self, database_name: str, collection_name: str, local_data_path: Path, root_dir: str) -> str:
        return self.__export_data_into_file_path(database_name, collection_name, local_data_path, root_dir)