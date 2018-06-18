docker run -it --rm \
  -p 8888:8888 \
  -p 6006:6006 \
  --name freeman \
  -e 'SNAPI_CONFIGS_PATH=/etc/configs/snapi.cfg' \
  -v ~/morgan-freeman:/morgan-freeman \
  -v ~/guang-deep-voice-conversion:/guang-deep-voice-conversion \
  -v ~/TIMIT:/data/private/vc/datasets/timit/TIMIT \
  -v ~/arctic:/data/private/vc/datasets/arctic \
  -v ~/freeman_log:/data/private/vc/logdir \
  -v ~/morgan-freeman/secrets:/etc/configs \
  guangyang/morgan-freeman:latest
