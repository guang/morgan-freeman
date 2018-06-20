# SR=22050
SR=22050

cd ~/tmp_preprocessing

for file in *.mp3
do
  /Users/guangyang/morgan-freeman/scripts/resample.py "$file" "${file/mp3/wav}" $SR
done
