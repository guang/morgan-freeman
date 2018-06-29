tag=latest

docker rm snapi
docker run -it --rm \
  --name snapi \
  -p 0.0.0.0:5000:5000 \
  -e 'HOME=/home/dev' \
  -e 'SNAPI_CONFIGS_PATH=/home/dev/morgan-freeman/secrets/snapi.cfg' \
  -e 'PYTHONPATH=/home/dev/morgan-freeman/snapi:/home/dev/morgan-freeman' \
  -v /Users/guangyang/morgan-freeman:/home/dev/morgan-freeman \
  -v /Users/guangyang/guang-deep-voice-conversion:/home/dev/guang-deep-voice-conversion \
  -v ~/morgan-freeman/secrets:/etc/configs \
  -v ~/s3_model:/s3_data/model \
  -v ~/freeman_tmp:/tmp \
  -v ~/.aws:/home/dev/.aws \
  guangyang/morgan-freeman-cpu:${tag} /bin/bash
#  guangyang/morgan-freeman-cpu:${tag} /bin/bash
#  -v ~/morgan-freeman/hparams:/hparams \
