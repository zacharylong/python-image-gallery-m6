#!/usr/bin/bash

export IMAGE_GALLERY_BOOTSTRAP_VERSION="1.0"

aws s3 cp s3://zacs-m6-image-gallery-config/ec2-prod-latest.sh ./
/usr/bin/bash ec2-prod-latest.sh
