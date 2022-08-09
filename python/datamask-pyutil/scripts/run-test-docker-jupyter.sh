#!/bin/bash

docker kill datamask-jupyter
docker rm datamask-jupyter

docker run -d --name  datamask-jupyter  -p 8888:8888  -v `pwd`/data:/datamask/data -v `pwd`:/datamask/src datamask-jupyter
sleep 2
docker logs datamask-jupyter

