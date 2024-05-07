import logging

from api_nichotined import Api, BigQuery


class TestApi(Api):
    def __init__(self):
        super().__init__("https://restcountries.com")

    def get_upload(self):
        return self.get(path="/v3.1/name/indonesia")

    @classmethod
    def init_bigquery(cls):
        bq = BigQuery()

        bq.authenticate_client_with_json_cred_path("cred.json")
        res = bq.get_rows_from(query="""SELECT * FROM `dummy` LIMIT 1000""")
        assert type(res[0].column_a) == str


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    response = TestApi().get_upload()
    assert response.is_array() is True
    assert response.is_success() is True

    # TestApi.init_bigquery()
