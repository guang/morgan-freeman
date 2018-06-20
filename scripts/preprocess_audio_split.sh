IN_PATH='/Users/guangyang/tmp_preprocessing'
TIME=3
mkdir /Users/guangyang/tmp_preprocessing_split
cd ${IN_PATH}
find . -name '*.wav' \
 -exec sh -c 'mkdir -p /Users/guangyang/tmp_preprocessing_split/$(dirname "{}")' \; \
 -exec sox {} /Users/guangyang/tmp_preprocessing_split/{}  trim 0 ${TIME} : newfile : restart \;
