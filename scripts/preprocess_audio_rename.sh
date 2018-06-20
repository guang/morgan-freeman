# TARGET="/Users/guangyang/idk_wat"
TARGET=$1

cp -r "$TARGET" /Users/guangyang/tmp_preprocessing
cd /Users/guangyang/tmp_preprocessing
counter=1

for file in *.mp3
do
  mv "$file" "$counter.mp3"
  counter=$(($counter+1))
done
