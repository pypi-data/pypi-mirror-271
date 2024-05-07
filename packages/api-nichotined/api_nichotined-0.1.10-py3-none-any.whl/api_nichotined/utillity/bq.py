import os

from google.cloud import bigquery
from google.cloud.bigquery import job


class BigQuery:
    def __init__(self):
        self._client = None

    @property
    def client(self) -> bigquery.Client:
        return self._client

    @client.setter
    def client(self, new_client: bigquery.Client):
        self._client = new_client

    @client.deleter
    def client(self):
        del self._client

    def authenticate_client_with_json_cred_path(self, json_cred_path: str):
        """
        Initialize BigQuery client
        :param json_cred_path: path of credential file
        """
        if os.path.exists(json_cred_path):
            self.client = bigquery.Client.from_service_account_json(json_credentials_path=json_cred_path)
        else:
            raise FileNotFoundError("JSON file cannot be located")

    def run_query(self, query) -> job.QueryJob:
        """
        Run a SQL query and return QueryJob.
        :param query: query in string
        :return: Query Job object
        """
        return self.client.query(query)

    def get_rows_from(self, query):
        """
        Run a SQL query and return list of rows
        :param query: query in string
        :return: A List of rows
        """
        rows = self.run_query(query)
        result = []
        for row in rows:
            result.append(row)
        return result
