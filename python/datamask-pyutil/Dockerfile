ARG build_var
FROM openjdk:8u265  as datamask_python

USER root

ENV PYTHON_VERSION=3.7

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
    python${PYTHON_VERSION} \
    python3-venv \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    python${PYTHON_VERSION}-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /datamask
WORKDIR /datamask

RUN python3 -m pip install --upgrade pip wheel setuptools && \
    python3 -m pip cache purge

COPY ./requirements.txt /datamask/
COPY ./scripts/create_venv.sh scripts/
COPY ./scripts/prepare_venv.sh scripts/
COPY ./scripts/activate_venv.sh scripts/
RUN bash scripts/create_venv.sh && \
    bash scripts/prepare_venv.sh && \
    pip3 cache purge

##################################################
FROM datamask_python as pre-builder-test

WORKDIR /datamask

COPY ./scripts/create-db-test.sh scripts/
COPY ./scripts/clean-tests.sh scripts/
RUN bash scripts/clean-tests.sh && \
    . scripts/activate_venv.sh && \
    bash scripts/create-db-test.sh 

RUN tar zcvf metastore_db.tar.gz ./metastore_db

COPY ./ /datamask

RUN bash scripts/clean.sh && \
    bash scripts/build.sh

##################################################
FROM datamask_python as build-test
COPY --from=pre-builder-test /datamask/artifact /datamask/artifact
COPY --from=pre-builder-test /datamask/metastore_db.tar.gz /datamask
RUN tar xvf metastore_db.tar.gz && rm -rf metastore_db.tar.gz

##################################################
FROM datamask_python as pre-builder-main

WORKDIR /datamask

COPY ./ /datamask

RUN bash scripts/clean.sh && \
    bash scripts/build.sh
##################################################
FROM datamask_python as build-main
COPY --from=pre-builder-main /datamask/artifact /datamask/artifact

##################################################
FROM build-${build_var} as datamask

WORKDIR /datamask

ENV ARTIFACT_PREFIX=artifact
ENV JSON_PARMS="test/test_parms/test_parms.json"
ENV JOB_NAME="TestRent"
ENV PARTITION_LIST="offset=4,offset=1"
ENV VERBOSE="-v -v"

CMD . scripts/activate_venv.sh && bash artifact/datamask-pyutil.sh "$ARTIFACT_PREFIX" "$JSON_PARMS" "$JOB_NAME" "$PARTITION_LIST" "$VERBOSE"
