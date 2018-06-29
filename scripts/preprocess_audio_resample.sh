# SR=22050
SR=22050

cd ${HOME}/tmp_preprocessing

for file in *.mp3
do
  ${HOME}/morgan-freeman/scripts/resample.py "$file" "${file/mp3/wav}" $SR
done
