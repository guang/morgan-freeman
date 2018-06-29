IN_PATH="${HOME}/tmp_preprocessing"
TIME=3
rm -rf ${HOME}/tmp_preprocessing_split
mkdir ${HOME}/tmp_preprocessing_split
cd ${IN_PATH}
find . -name '*.wav' \
 -exec sh -c "mkdir -p ${HOME}/tmp_preprocessing_split/$(dirname '{}')" \; \
 -exec sox {} ${HOME}/tmp_preprocessing_split/{}  trim 0 ${TIME} : newfile : restart \;
