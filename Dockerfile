FROM homdx/kivymd-store:004

#ARG WORK_DIR=/home/user/hostcwd

ADD . ${WORK_DIR}/app2

RUN sudo chown user -R ${WORK_DIR}/app2 && sudo apt-get install aria2 --yes

ARG DOT_VERSION=0.0.2

ARG DOT_HASH=e36c529b42f0e8ef2ea334bdb662c2e1136dc0fd8316366bde82e9c557fe350f
ARG DOT_PATH=https://github.com/homdx/Muhna/releases/download
ARG DOT_FILE=buildozer-python2.tar.gz

ARG DISABLECACHE

RUN set -ex && \
    if [ -z "$DISABLECACHE" ] ; \
    then echo 'Now enable Cached files for Python2 files. If you not need cache build with: --build-arg DISABLECACHE=something'; \
    set -ex ; \
    cd ${WORK_DIR}/app2 ; sudo time -p aria2c -x 5 ${DOT_PATH}/${DOT_VERSION}/${DOT_FILE} ; \
    echo "${DOT_HASH}  ${DOT_FILE}" | sha256sum -c ; \
    time -p sudo tar -xf ${DOT_FILE} ; sudo rm ${DOT_FILE} ; \
    else echo Cache are disabled = $DISABLECACHE; \
    # Build full version \
    cd ${WORK_DIR}/app2 ; \
    echo build Full version; \
    fi

RUN cd app2 && time buildozer android debug || sudo cp /home/user/hostcwd/app2/.buildozer/android/platform/build/dists/muhna/bin/Muhna-*-debug.apk /home/user/Muhna-py2.apk

CMD tail -f /var/log/faillog

