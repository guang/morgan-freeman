# TARGET="/Users/guangyang/idk_wat/*"
TARGET=$1

rm -rf ${HOME}/tmp_preprocessing
cp -r "$TARGET" ${HOME}/tmp_preprocessing
cd ${HOME}/tmp_preprocessing
counter=1

for file in *.mp3
do
  mv "$file" "$counter.mp3"
  counter=$(($counter+1))
done
