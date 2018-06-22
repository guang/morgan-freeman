docker run -it --rm \
  -p 8888:8888 \
  -p 6006:6006 \
  --name freeman \
  -e 'SNAPI_CONFIGS_PATH=/etc/configs/snapi.cfg' \
  -v ~/morgan-freeman:/morgan-freeman \
  -v ~/guang-deep-voice-conversion:/guang-deep-voice-conversion \
  -v ~/TIMIT:/freeman_data/TIMIT \
  -v ~/inference:/freeman_data/inference \
  -v ~/s3_model:/freeman_data/logdir \
  -v ~/morgan-freeman/secrets:/etc/configs \
  guangyang/morgan-freeman:latest
