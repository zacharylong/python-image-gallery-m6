import os
from .secrets import get_secret_s3_key, get_secret_s3_secret

# hard coded from new IAM role for bucket only access

#S3_BUCKET = os.environ.get("S3_BUCKET")
S3_BUCKET = "zacs-m6-image-gallery"
#S3_KEY = os.environ.get("S3_KEY")
S3_KEY = get_secret_s3_key()
#S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_SECRET = get_secret_s3_secret()