import os
import json
import boto3
from botocore.exceptions import ClientError


class MinIOStorage:
    def __init__(self):
        endpoint = os.environ.get("MINIO_ENDPOINT")
        access_key = os.environ.get("MINIO_ACCESS_KEY")
        secret_key = os.environ.get("MINIO_SECRET_KEY")

        missing = [name for name, val in [
            ("MINIO_ENDPOINT", endpoint),
            ("MINIO_ACCESS_KEY", access_key),
            ("MINIO_SECRET_KEY", secret_key),
        ] if not val]

        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

        self._s3 = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def save(self, kpis):
        try:
            self._s3.create_bucket(Bucket="crypto-kpis")
        except self._s3.exceptions.BucketAlreadyOwnedByYou:
            pass
        except ClientError as e:
            if e.response["Error"]["Code"] != "BucketAlreadyExists":
                raise

        try:
            self._s3.put_object(
                Bucket="crypto-kpis",
                Key="latest.json",
                Body=json.dumps(kpis, indent=2),
                ContentType="application/json",
            )
        except ClientError as e:
            raise RuntimeError(f"Failed to save KPIs to MinIO: {e}")

    def load(self):
        return self._s3.get_object(Bucket="crypto-kpis", Key="latest.json")
