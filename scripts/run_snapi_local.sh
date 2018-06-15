tag=latest

docker rm snapi
docker run -it --rm \
  --name snapi \
  -p 0.0.0.0:5000:5000 \
  -e 'HOME=/home/dev' \
  -e 'SNAPI_CONFIGS_PATH=/home/dev/morgan-freeman/secrets/snapi.cfg' \
  -e 'PYTHONPATH=/home/dev/morgan-freeman/snapi' \
  -v /Users/guangyang/morgan-freeman:/home/dev/morgan-freeman \
  guangyang/snapi:${tag} python /home/dev/morgan-freeman/snapi/app.py
