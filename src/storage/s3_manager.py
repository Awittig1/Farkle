import boto3, json

class S3Manager:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client("s3")
        self.bucket = bucket_name

    def upload_scores(self, players: list):
        data = {p.name: p.score for p in players}
        self.s3.put_object(Bucket=self.bucket, Key="leaderboard.json", Body=json.dumps(data))