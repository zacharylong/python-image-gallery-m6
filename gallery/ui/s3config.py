import os

# hard coded from new IAM role for bucket only access

#S3_BUCKET = os.environ.get("S3_BUCKET")
S3_BUCKET = "zacs-m6-image-gallery"
S3_KEY = os.getenv("S3_KEY")
#S3_KEY = get_secret_s3_key()
S3_SECRET = os.getenv("S3_SECRET_ACCESS_KEY")
#S3_SECRET = get_secret_s3_secret()