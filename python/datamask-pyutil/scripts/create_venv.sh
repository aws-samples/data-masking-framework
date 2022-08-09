#/bin/bash

pybin=`find /usr/bin /usr/local/bin  -regex ".*python3\.*[5-7]*" | sort -r | head -1`

pyversion=`${pybin} --version 2> /dev/null`
if [[ $? -ne 0 ]]; then echo "ERROR: Python 3 not installed."; exit 1; fi

pymversion=`echo $pyversion | awk '{print substr($2,3,1)}'`
if [ $pymversion != "8" ]; then echo "Python version is ${pyversion}"; else echo "ERROR: Python version is ${pyversion}. Python 3 must be different of 3.8"; exit 1; fi

${pybin} -m venv .venv
 
