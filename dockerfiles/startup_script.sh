#!/bin/sh

# pull models
aws s3 sync s3://bwhoyouwant2-be-data/model/current/ /s3_data/model/current/.
