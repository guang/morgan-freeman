#!/bin/sh

# TODO: use dis if/when we be doing them deploy keys on private repos yo
# # Use deployment keys to clone repos
# eval `ssh-agent`
# chmod 400 /home/dev/.ssh/deploy-snapi
# 
# # in case the id_rsa is not attached (hence no /root/.ssh dir)
# mkdir -p /root/.ssh
# touch /root/.ssh/known_hosts
# ssh-keyscan github.com >> /root/.ssh/known_hosts
# ssh-add /home/dev/.ssh/deploy-snapi
git clone https://github.com/guang/morgan-freeman.git

# cd ${HOME}/snapi
# git checkout ${SNAPI_BRANCH_NAME}
