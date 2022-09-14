 

## 						   Data-Masking-Framework

Data Masking Framework (DMF) is a configuration driven approach to mask sensitive data using hashing or encryption in an AWS Data Lakes. This uses PySpark with EMR or Glue based environment. The configuration contains Glue catalog tables and columns and the associated data masking approach. The data masking uses the following following are the used for data masking. 

1. Reversible data encryption using a key

2. Non-reversible data masking using hashing algorithm (sha256, sha512)

 This framework also supports key based lookup using the original data. 

This project has two main components.

A python util to for the basic datamasking process

See [datamask-pyutil](https://github.com/aws-samples/data-masking-framework/blob/main/python/datamask-pyutil/README.md) for more information.

EMR-launch stack to make the process automated. 

See [datamask-emr-launch](https://github.com/aws-samples/data-masking-framework/blob/main/stacks/datamask-emr-launch/README.md) for more information.

 