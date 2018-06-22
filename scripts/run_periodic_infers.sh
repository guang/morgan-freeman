set -e
# train1='20180611-00'
train1=$1
# train2='1/20180621-00'
train2=$2


while true
do
  python /morgan-freeman/infer.py $train1 $train2
  aws s3 sync /freeman_data/inference s3://bwhoyouwant2-be-data/inference
  sleep 600
done
