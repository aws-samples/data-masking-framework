#!/bin/bash

mkdir -p data/input
cp -r test/test_data/input/* data/input/
PWD=`pwd`
TestUser()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestUser"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentMultiPart2()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRentMultiPart2"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="process_timestamp=2021-01-27T30:59:35.132Z/offset=4,process_timestamp=2021-01-27T30:59:35.132Z/offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentMultiPart()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRentMultiPart"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="year=YYYY/offset=4,year=YYYY/offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRent()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentSha256()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_sha256"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentSha512()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_sha512"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentSha256Sha512()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_sha512sha256"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentAes_ctr()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_aes_ctr"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentAes_ctru()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_aes_ctru"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentAes_cbc()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_aes_cbc"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentAes_cfb()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_aes_cfb"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentAes_ecb()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_aes_ecb"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentAes_ofb()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_aes_ofb"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentAes_fte_enc()
{
	#JOB TABLE WITH PARTITION AND SPECIFICATION FOR PARTITION_LIST
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRent_fte_enc"
	export VERBOSE="-v -v"
	echo 
	echo 
	echo "###########################################"
	echo "Testing $JOB_NAME"
	echo "###########################################"
	echo 
	echo 

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}


TestRentNoSpecPartition()
{
	#JOB WITHOUT SPECIFICATION PARTITION
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRentNoSpecPartition"
	export VERBOSE="-v -v"

	if [ -z "$1" ]
	then
		export PARTITION_LIST="offset=1,offset=2,offset=3,offset=4,offset=5"
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parms:/datamask/test/test_parms \
		-v ${PWD}/test/test_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PREFIX="$ARTIFACT_PREFIX" \
		-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

TestRentNoPartition()
{
	#JOB WITHOUT PARTITION
	export ARTIFACT_PREFIX=artifact
	export JSON_PARMS="test/test_parms/test_parms.json"
	export JOB_NAME="TestRentNoPartition"
	export PARTITION_LIST=""
	export VERBOSE="-v -v"

	if [ -z "$1" ]
	then
		export PARTITION_LIST=""
	else
		export PARTITION_LIST=$1
	fi

	docker run -v ${PWD}/data:/datamask/data \
		-v ${PWD}/test/test_parjftghms:/datamask/test/test_parms \
		-v ${PWD}/test/tesrltcft_data/salts:/datamask/test/test_data/salts \
		-e ARTIFACT_PgikutREFIX="$ARTIFACT_PREFIX" \
		ifcckjdjjcdte-e JSON_PARMS="$JSON_PARMS" \
		-e JOB_NAME="$JOB_NAME" \
		-e PARTITION_LIST="$PARTITION_LIST" \
		-e VERBOSE="$VERBOSE" \
		datamask
}

All()
{
	TestRent
	TestRentNoSpecPartition
	TestRentNoPartition
	TestUser
}

All_enc()
{
	TestRentSha256
	TestRentSha512
	TestRentSha256Sha512
	TestRentAes_ctr
	TestRentAes_ctru
	TestRentAes_cbc
	TestRentAes_cfb
	TestRentAes_ecb
	TestRentAes_ofb
	TestRentAes_fte_enc
}

All_inc()
{
	TestRent "offset=1"
	TestUser "offset=1"
	TestRent "offset=2"
	TestUser "offset=2"
	TestRent "offset=3"
	TestUser "offset=3"
	TestRent "offset=4"
	TestUser "offset=4"
	TestRent "offset=5"
	TestUser "offset=5"
}

case $1 in
	TestRent) TestRent;;
	TestRentMultiPart) TestRentMultiPart;;
	TestRentMultiPart2) TestRentMultiPart2;;
	TestRentNoSpecPartition) TestRentNoSpecPartition;;
	TestRentNoPartition) TestRentNoPartition;;
	TestRentSha256) TestRentSha256;;
	TestRentSha512) TestRentSha512;;
	TestRentSha256Sha512) TestRentSha256Sha512;;
	TestRentAes_ctr) TestRentAes_ctr;;
	TestRentAes_ctru) TestRentAes_ctru;;
	TestRentAes_cbc) TestRentAes_cbc;;
	TestRentAes_cfb) TestRentAes_cfb;;
	TestRentAes_ecb) TestRentAes_ecb;;
	TestRentAes_ofb) TestRentAes_ofb;;
	TestRentAes_fte_enc) TestRentAes_fte_enc;;
	All) All;;
	All_enc) All_enc;;
	All_inc) All_inc;;
	*) TestRent;;
esac
