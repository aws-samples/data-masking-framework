# -*- coding: utf-8 -*-
"""

"""
from datamask_pyutil.utility import get_json_s3, get_json_local, delete_path_s3, delete_path_local, exists_files_s3, exists_files_local
from jsonschema import validate
import datetime 
import json
import logging
import hashlib
import re
import uuid
import pyaes
import os
import secrets
import pyffx
import binascii
import base64


_logger = logging.getLogger(__name__) 

class DatamaskConfProcessError(Exception):
    pass

class DatamaskConfProcess:
    """DatamaskConfProcess Constructor 
        This is the DatamaskConfProcess class to be used in datamask processes

        The constructor validate the JSON parameter file format with the schema above and set private variables: domains, salts and job.

        :param config_path:
        :type config_path: str
        Path to the JSON parameter file 
        :param jobName:
        Jobname to be searched inside the parameter file 
        :type jobName: str
    """

    def __init__(self, config_path: str, jobName: str):
        """Constructor method"""
        self.__schema = {
            "title": "DatamaskConfProcess",
            "type": "object",
            "description": "JSON schema to the datamask-pyutil parameter file", 
            "properties": {
                "Jobs": {
                    "description": "List of Jobs",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "JobName": { "type": "string", "description": "The Job name" },
                            "Active": { "type": "boolean", "description": "If False turn off the job processing" },
                            "Input": {
                                "type": "object",
                                "description": "Input properties",
                                "properties": {
                                    "InputPath": { "type": "string", "description": "The input path to be read" },
                                    "Delete": { "type": "boolean", "description": "The input path to be read" },
                                    "RepartitionValue": { "type": "number", "description": "If set the process will try to repartition the input to better performance" },
                                    "ReadFormat": { "type": "string", "description": "The read format, Examples: parquet, csv " },
                                    "PartitionColumnTypeInference": {"type": "boolean", "description": "Disable or Enable partition name inference type on input. Default: True"},
                                    "IntPartitions": {
                                        "type": "array",
                                        "description": "If input has partitions keys, this is the list of int partitions",
                                        "items": { "type": "string"}
                                        },
                                    "ReadOptions": { 
                                        "type": "array", 
                                        "items": {
                                            "type": "object",
                                            "description": "The read options to use in the read process",
                                            "properties": {
                                                "OptionName": { "type": "string", "description": "Option name" },
                                                "OptionValue": { "type": "string", "description": "Option Value" }
                                                },
                                                "additionalProperties": False,
                                                "required": ["OptionName", "OptionValue"]
                                            } 
                                        }
                                    },
                                "additionalProperties": False,
                                "required": ["InputPath", "ReadFormat"]
                                },
                            "Output": {
                                "type": "object",
                                "description": "Output properties",
                                "properties": {
                                    "OutputPath": { "type": "string", "description": "The output path to write"  },
                                    "OutputTable": { "type": "string", "description": "If set the process will try to update the table metadata"   },
                                    "OutputDatabase": { "type": "string", "description": "If set the process will try to update the metadata, it needs to be set with  OutputTable"   },
                                    "Coalesce": { "type": "number", "description": "If set the process will coalesce partitions before write in the output. This is usually the number of files to be write in the ouput path."   }
                                    },
                                "additionalProperties": False,
                                "required": ["OutputPath"]
                                },
                            "MaskFields": {
                                "type": "array",
                                "description": "List of Mask Field properties",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "Active": { "type": "boolean", "description": "If False turn off the mask field"   },
                                        "MaskFieldName": { "type": "string", "description": "Mask field name"   },
                                        "FieldName": { "type": "string", "description": "Filed Name"   },
                                        "FormatRE": { "type": "string", "description": "Regular expression RE to be procced. Use this expression to use just a field part"   },
                                        "DomainName": { "type": "string", "description": "Domain name to get mask configurations"   },
                                        "KeepMaskName": { "type": "boolean", "description": "If True process will keep the mask name, otherwise the mask field will renamed to the original field name"  }
                                        },
                                "additionalProperties": False,
                                    "required": ["Active", "MaskFieldName", "FieldName", "DomainName"] 
                                    }
                                }
                            },
                            "additionalProperties": False,
                            "required": ["JobName", "Active", "Input", "Output", "MaskFields"]
                        }
                },
                "Domains": {
                    "type": "array",
                    "description": "List of data mask domains",
                    "items": {
                        "type": "object",
                        "properties": {
                            "DomainName": { "type": "string" , "description": "Domain name"  }, 
                            "SaltName": { "type": "string", "description": "The sal name to be searched inside the sal file"  }, 
                            "Layout": { "type": "string", "description": "Layout to be used to replace the salt and field. $SALT will be replaced by the sal value and $VALUE will be replaced by the field value" }, 
                            "MaskType": { "type": "string", "description": "Algorithm type to mask the field" }, 
                            "EncryptKey": {"type": "string", "description": "Encryption key for Algorithm, only when you use aes_ctr and fte "},
                            "FieldAlias": { "type": "string", "description": "Field alias to be used in the Reverse dataset" }, 
                            "MaskFieldAlias": { "type": "string", "description": "Mask field alias to be used in the reverse dataset" }, 
                            "ReverseDataset": { 
                                "type": "object", 
                                "properties": {
                                    "Active": { "type": "boolean", "description": "If False tur off the creation of the reverse dataset" },
                                    "DatasetPath": { "type": "string", "description": "Reverse dataset path" }, 
                                    "BackupDatasetPath": { "type": "string", "description": "Reverse backup dataset path" }, 
                                    "BackupDatasetPartitionLabels": { 
                                        "type": "object",
                                        "description": "Backup Dataset Partition Labels",
                                        "properties": { 
                                            "Year": { "type": "string", "description": "Backup Dataset Partition year Label" }, 
                                            "Month": { "type": "string", "description": "Backup Dataset Partition month Label" }, 
                                            "Day": { "type": "string", "description": "Backup Dataset Partition day Label" }, 
                                            "Hour": { "type": "string", "description": "Backup Dataset Partition hour Label" }, 
                                            "Id": { "type": "string", "description": "Backup Dataset Partition id Label" }
                                            }
                                        },
                                    "BackupCoalesce": { "type": "number", "description": "If set the process will coalesce partitions before write in the reverse dataset. This is usually the number of files to be write in the ouput path" }, 
                                    "Coalesce": { "type": "number", "description": "If set the process will coalesce partitions before write in the reverse dataset. This is usually the number of files to be write in the ouput path" }, 
                                    "KeepOnlyBackup": { "type": "boolean", "description": "If True only the backup table will be avaiable, Dafault False" },
                                    "JobNamePartition": { "type": "boolean", "description": "If set it will enable TableName Partition, Default False" },
                                    "JobNamePartitionFieldName": { "type": "string", "description": "Change the default field Name, Default 'JobName'" },
                                    "HashBucketing": { "type": "boolean", "description": "If set the process will create bucketing in partitions" }, 
                                    "ReverseTable": { "type": "string", "description": "If set the process will try to update the table metadata"   },
                                    "ReverseDatabase": { "type": "string", "description": "If set the process will try to update the metadata, it needs to be set with  ReverseTable"   },
                                    },
                                "additionalProperties": False,
                                "required": ["Active", "DatasetPath"]
                                } 
                            },
                            "additionalProperties": False,
                            "required": ["DomainName", "Layout","MaskType", "FieldAlias", "MaskFieldAlias"]
                        }
                },
                "Salts": {
                    "type": "object",
                    "description": "Salt properties",
                    "properties": {
                        "SaltsPath": { "type": "string", "description": "The salt path" }
                    },
                    "additionalProperties": False,
                    "required": ["SaltsPath"]
                }
              },
            "additionalProperties": False,
            "required": ["Jobs", "Domains"]
        } 

        if config_path.find("s3") == -1:
            config = get_json_local(config_path)
        else:
            config = get_json_s3(config_path)
        validate(instance=config, schema=self.__schema)        
        if not self.__set_job(jobName, config):
            raise DatamaskConfProcessError("jobName not found")
        self.__set_domains(config)
        self.__set_salts(config)
        self.__partition_keys = []
        return 

    def __set_domains(self, config: str):
        """ Set domains and generate a index to fast get

        :param config:
        :type config: str
        """
        domains_idx = {}
        domains = config["Domains"]
        idx = 0
        for d in domains:
            domains_idx[domains[idx]["DomainName"]]=idx 
            idx = idx + 1
        self.__domains = domains
        self.__domains_idx = domains_idx
        return

    def __set_salts(self, config: str):
        """ Validate the Salt file, parse the JSON file and generate a index to fast get.

        :param config:
        :type config: str
        """
        salt_schema = {
                "tittle": "Salf Json File",
                "type": "array",
                "description": "File to store the salts",
                "items": {
                    "type": "object",
                    "properties": {
                        "SaltName": {"type": "string", "description": "Salt name"},
                        "SaltValue": {"type": "string","description": "Salt Value"}
                        },
                        "additionalProperties": False,
                        "required": ["SaltName", "SaltValue"]
                    }
                }
        salt = None
        salt_idx = None
        if "Salts" in config:
            salt_path = config["Salts"]["SaltsPath"]
            if salt_path.find("s3") == -1:
                salt = get_json_local(salt_path) 
            else:
                salt = get_json_s3(salt_path) 
            salt_idx = {}
            validate(instance=salt, schema=salt_schema)        
            idx = 0
            for s in salt:
                salt_idx[salt[idx]["SaltName"]] = idx
                idx = idx + 1
        self.__salt = salt 
        self.__salt_idx = salt_idx 
        return

    def __set_job(self, jobName: str, config : str):
        """ Set the Job. 

        :param jobName:
        :type jobName: str
        :param config:
        :type config: str
        :return: True id the job was found and False if is not.
        :rtype: boolean
        """
        for job in config["Jobs"]:
            if jobName == job['JobName']:
                self.__job = job
                return True
        return False

    def is_job_active(self):
        """is_job_active.

        :return: True id the job is enable
        :rtype: boolean
        """
        return self.__job["Active"]

    def __get_input_delete(self):
        """__get_input_delete.

        :return: Return Input Delete 
        """
        if 'Delete' in self.__job['Input']: 
            return self.__job['Input']['Delete']
        else:
            return False

    def __get_input_read_format(self):
        """__get_input_read_format.

        :return: Return Input Read Format
        """
        return self.__job['Input']['ReadFormat']

    def __get_input_path(self):
        """__get_input_path.

        :return: Return Job Input path

        """
        return self.__job['Input']['InputPath']

    def __apply_input_read_options_spark(self, read_stm):
        """__apply_input_read_options_spark.
        Apply all the read options in the job properties

        :param read_stm: Spark read statement 
        :return: return a spark read statement with the read options applied
        """

        if 'ReadOptions' in self.__job['Input']:
            for option in self.__job['Input']['ReadOptions']:
                read_stm = read_stm.option(option['OptionName'], option['OptionValue'])
                ret = True
        return read_stm

    def __get_input_repart_value(self):
        """__get_input_repart_value.

        :return: return the repartition valeu or None if this properties was not set
        """
        if "RepartitionValue" in self.__job["Input"]:
            return self.__job["Input"]["RepartitionValue"]
        else:
            return None

    def __read_input_spark(self, spark):
        """__read_input_spark.

        :param spark: Spark session
        :return: return a spark dataframe with all the read properties
        """
        read_stm = spark.read.format(self.__get_input_read_format())
        read_stm = self.__apply_input_read_options_spark(read_stm)
        repart_value = self.__get_input_repart_value()
        df = read_stm.load(self.__get_input_path())
        if repart_value:
            _logger.info("Repartition value [{}]".format(repart_value))
            df = df.repartition(repart_value)
        return df

    def __get_input_read_int_partitions(self):
        """__get_input_read_int_partitions.
        :return: return the list of integer partition keys

        """
        if "IntPartitions" in self.__job['Input']:
            return self.__job['Input']['IntPartitions']
        else:
            return []

    def __get_where_clause_from_hive_part_list(self, hive_part_list: list):
        """__get_where_clause_from_hive_part_list.
        Generate a where clause to filter a dataframe.

        :param hive_part_list: List of partitions keys to be used in the where clause
        :type hive_part_list: list

        :return: return the whare clause
        :rtype: str
        """
        first_or = True
        where_clause = ''
        int_partitions = self.__get_input_read_int_partitions()
        partition_keys=[]
        for part in hive_part_list:
            where_clause_and = ''
            part_key_value_vet = part.split("/") 
            first_and = True
            for part_key_value in part_key_value_vet:
                part_key = part_key_value.split("=")
                if part_key[0] not in partition_keys:
                    partition_keys.append(part_key[0])
                if part_key[0] in int_partitions:
                    value = part_key[1]
                else:
                    value = "'{}'".format(part_key[1])
                if first_and:
                    where_clause_and = "{}={}".format(part_key[0],value)
                    first_and = False
                else:
                    where_clause_and = "{} AND {}={}".format(where_clause_and,part_key[0],value)
            if first_or:                    
                where_clause = '({})'.format(where_clause_and)
                first_or = False
            else:
                where_clause = '{} OR ({})'.format(where_clause,where_clause_and)
            self.__partition_keys = partition_keys
        return where_clause

    @staticmethod
    def __get_hash_sha256(text: str):
        """__get_hash_sha256.
        Get a hash sha256 based on text 

        :param text: Text to be hashed
        :type text: str

        :return: Hash value
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    def __get_hash_sha512(text: str):
        """__get_hash_sha512.
        Get a hash sha512 based on text

        :param text: Text to be hashed
        :type text: str

        :return: Hash value
        """
        return hashlib.sha512(text.encode('utf-8')).hexdigest()

    @staticmethod
    def __get_aes(input: str, key: str, inmode: str, salt: str):
        """__get_aes_ctr.
        Encrypts a string using AES algorithm

        :param input:  String to be encrypted
        :type layout: str
        :param key: Key to be used for the algorithm, Example: abcdefghijklmnopqrstuvwxascertgb
        :type layout: str
        :param inmode:  AES modes, Example: aes_ctr, aes_ctru, aes_cbc, aes_cfb, aes_ecb, aes_ofb
        :type layout: str
        :param salt:  String for salting
        :type layout: str
        """
        if input is None or inmode is None:
            _logger.error("Input is None for AES encrypt")
            return None

        if key is None or len(key) not in (16, 24, 32):
            _logger.error("Error in AES KEY")
            return None

        try:
            iterationCount = 1036
            inkey = hashlib.pbkdf2_hmac('sha256', key.encode('utf-8'), salt.encode('utf-8'), iterationCount)

            mode = str(inmode).lower()
            if mode == "aes_ctr":
                iv = secrets.randbits(256)
                aes = pyaes.AESModeOfOperationCTR(inkey, pyaes.Counter(iv))
                cipher_txt = aes.encrypt(input.encode())
                cipher_txt2 = binascii.hexlify(cipher_txt)
                return str(cipher_txt2.decode('utf-8')) + "|" + str(iv)
            elif mode == "aes_ctru":
                aes = pyaes.AESModeOfOperationCTR(inkey)
                cipher_txt = aes.encrypt(input.encode())
                cipher_txt2 = binascii.hexlify(cipher_txt)
                return str(cipher_txt2.decode('utf-8'))
            elif mode == "aes_cbc":
                iv = os.urandom(16)
                encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(inkey, iv=iv))
                ciphertext = encrypter.feed(input.encode())
                ciphertext += encrypter.feed()
                ciphertext = base64.b64encode(ciphertext)
                cipher_txt2 = binascii.hexlify(ciphertext)
                iv_mod = binascii.hexlify(iv)
                return str(cipher_txt2.decode('utf-8')) + "|" + str(iv_mod.decode('utf-8'))
            elif mode == "aes_cfb":
                iv = os.urandom(16)
                segment_size = 16
                encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationCFB(inkey, iv=iv, segment_size=segment_size))
                ciphertext = encrypter.feed(input.encode())
                ciphertext += encrypter.feed()
                ciphertext = base64.b64encode(ciphertext)
                cipher_txt2 = binascii.hexlify(ciphertext)
                iv_mod = binascii.hexlify(iv)
                return str(cipher_txt2.decode('utf-8')) + "|" + str(iv_mod.decode('utf-8')) + "|" + str(segment_size)
            elif mode == "aes_ecb":
                encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationECB(inkey))
                ciphertext = encrypter.feed(input.encode())
                ciphertext += encrypter.feed()
                ciphertext = base64.b64encode(ciphertext)
                cipher_txt2 = binascii.hexlify(ciphertext)
                return str(cipher_txt2.decode('utf-8'))
            elif mode == "aes_ofb":
                iv = os.urandom(16)
                aes = pyaes.AESModeOfOperationOFB(inkey, iv=iv)
                cipher_txt = aes.encrypt(input.encode())
                cipher_txt2 = binascii.hexlify(cipher_txt)
                iv_mod = binascii.hexlify(iv)
                return str(cipher_txt2.decode('utf-8')) + "|" + str(iv_mod.decode('utf-8'))
        except Exception as ne:
            _logger.error("Exception Encrypt: {}".format(ne))

    @staticmethod
    def __get_daes(input: str, key: str, inmode: str, salt: str):
        """__get_aes_ctr.
        Decrypts a string using AES algorithm

        :param input:  String to be encrypted
        :type layout: str
        :param key: Key to be used for the algorithm, Example: abcdefghijklmnopqrstuvwxascertgb
        :type layout: str
        :param inmode:  AES modes, Example: aes_ctr, aes_ctru, aes_cbc, aes_cfb, aes_ecb, aes_ofb
        :type layout: str
        :param salt:  String for salting
        :type layout: str
        """
        if input is None or inmode is None:
            _logger.error("Input is None for AES encrypt")
            return None

        if key is None or len(key) not in (16, 24, 32):
            _logger.error("Error in AES KEY")
            return None

        try:
            iterationCount = 1036
            inkey = hashlib.pbkdf2_hmac('sha256', key.encode('utf-8'), salt.encode('utf-8'), iterationCount)

            mode = str(inmode).lower()
            if mode == "aes_ctr":
                msg, iv = input.split('|')
                aes = pyaes.AESModeOfOperationCTR(inkey, pyaes.Counter(int(iv)))
                encrypted_msg2 = binascii.unhexlify(msg)
                decrypted_msg2 = aes.decrypt(encrypted_msg2)
                return str(decrypted_msg2.decode('utf-8'))
            elif mode == "aes_ctru":
                msg = input
                aes = pyaes.AESModeOfOperationCTR(inkey)
                encrypted_msg2 = binascii.unhexlify(msg)
                decrypted_msg2 = aes.decrypt(encrypted_msg2)
                return str(decrypted_msg2.decode('utf-8'))
            elif mode == "aes_cbc":
                msg, iv = input.split('|')
                iv_mod = binascii.unhexlify(iv)
                decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(inkey, iv=iv_mod))
                encrypted_msg2 = binascii.unhexlify(msg)
                decrypted = decrypter.feed(base64.b64decode(encrypted_msg2))
                decrypted += decrypter.feed()
                return str(decrypted.decode('utf-8'))
            elif mode == "aes_cfb":
                msg, iv, segment_size = input.split('|')
                iv_mod = binascii.unhexlify(iv)
                seg_size = int(segment_size)
                decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCFB(inkey, iv=iv_mod, segment_size=seg_size))
                encrypted_msg2 = binascii.unhexlify(msg)
                decrypted = decrypter.feed(base64.b64decode(encrypted_msg2))
                decrypted += decrypter.feed()
                return str(decrypted.decode('utf-8'))
            elif mode == "aes_ecb":
                msg = input
                decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(inkey))
                encrypted_msg2 = binascii.unhexlify(msg)
                decrypted = decrypter.feed(base64.b64decode(encrypted_msg2))
                decrypted += decrypter.feed()
                return str(decrypted.decode('utf-8'))
            elif mode == "aes_ofb":
                msg, iv = input.split('|')
                iv_mod = binascii.unhexlify(iv)
                aes = pyaes.AESModeOfOperationOFB(inkey, iv=iv_mod)
                encrypted_msg2 = binascii.unhexlify(msg)
                decrypted_msg2 = aes.decrypt(encrypted_msg2)
                return str(decrypted_msg2.decode('utf-8'))
        except Exception as ne:
            _logger.error("Exception Encrypt: {}".format(ne))

    @staticmethod
    def __get_fte_encrypt(input: str, key: str, masktype: str):
        """__get_fte_encrypt.
               Encrypts a string using FTE algorithm

               :param input:  String to be encrypted
               :type layout: str
               :param key: Key to be used for the algorithm, Example: abcdefghijklmnopqrstuvwxascertgb
               :type layout: str
               :param masktype: Mask type to get the digits, Example: fte_enc, fte_enc_1, fte_enc_12
               :type layout: str
               """
        if input is None:
            return None

        if key is None or len(key) not in (16, 24, 32):
            _logger.error("Error in FTE KEY")
            return None

        try:

            printable = ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
            input_v = input
            key_v = key
            def get_fpe(input_v, key_v):
                if input_v.isdigit():
                    text_enc = pyffx.Integer(key_v.encode('utf-8'), length=len(input_v))
                else:
                    text_enc = pyffx.String(key_v.encode('utf-8'), alphabet=printable, length=len(input_v))
                encrypt_v = str(text_enc.encrypt(input_v))
                if input_v.isdigit() and len(encrypt_v) < len(input_v):
                    encrypt_v = str(encrypt_v).rjust(len(input_v), '0')
                return encrypt_v

            fte_val = masktype.split("_")
            if fte_val != None and len(fte_val) >= 3:
                encryptn = int(fte_val[2] or 0)
                if encryptn != 0 and int(encryptn) < len(input):
                    digcypher = get_fpe(input[0:encryptn], key)
                    rdigcypher = input[encryptn:len(input)]
                    encrypt = digcypher + rdigcypher
                else:
                    encrypt = get_fpe(input, key)
            else:
                encrypt = get_fpe(input, key)
            return encrypt
        except Exception as ne:
            print("Exception FTE Encrypt: {}".format(ne))

    @staticmethod
    def __get_fte_dcrypt(input: str, key: str, masktype:str):
        """__get_fte_dcrypt.
        Decrypts a string using FTE algorithm

        :param input:  String to be decrypted
        :type layout: str
        :param key: Key to be used for the algorithm, Example: abcdefghijklmnopqrstuvwxascertgb
        :type layout: str
        :param masktype: Mask type to get the digits, Example: fte_enc, fte_enc_1, fte_enc_12
        :type layout: str
        """
        if input is None:
            return None

        if key is None or len(key) not in (16, 24, 32):
            _logger.error("Error in FTE KEY")
            return None

        try:
            printable = ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

            def get_dfpe(input_v, key_v):
                if input_v.isdigit():
                    text_enc = pyffx.Integer(key_v.encode('utf-8'), length=len(input_v))
                else:
                    text_enc = pyffx.String(key_v.encode('utf-8'), alphabet=printable, length=len(input_v))
                decrypt_v = str(text_enc.decrypt(input_v))
                if input_v.isdigit() and len(decrypt_v) < len(input_v):
                    decrypt_v = str(decrypt_v).rjust(len(input_v), '0')
                return decrypt_v

            fte_val = masktype.split("_")
            if fte_val != None and len(fte_val) >= 3:
                encryptn = int(fte_val[2] or 0)
                if encryptn != 0 and int(encryptn) < len(input):
                    digcypher = get_dfpe(input[0:encryptn], key)
                    rdigcypher = input[encryptn:len(input)]
                    decrypt = digcypher + rdigcypher
                else:
                    decrypt = get_dfpe(input, key)
            else:
                decrypt = get_dfpe(input, key)
            return decrypt
        except Exception as ne:
            print("Exception FTE Encrypt: {}".format(ne))


    @staticmethod
    def __get_hash_sha512_256(text: str):
        """__get_hash_sha512_256.
        Get a hash sha256 and sha512 based on text

        :param text:
        :type text: str

        :return: Hash value
        """
        return DatamaskConfProcess.__get_hash_sha256(DatamaskConfProcess.__get_hash_sha512(text))

    @staticmethod
    def __mask(text, salt, layout: str, mask_type: str, format_re: str, key=str):
        """__mask.
        Mask a text entries based on parameters

        :param text:  Text to be masked
        :param salt: Salt value to be used in before mask
        :param layout: Layout to be used to replace the salt value and the field value. $VALUE will be replaced to the field value and $SALT will be replaced to the salt value
        :type layout: str 
        :param mask_type: Type of algorithms Sha256, sha512, others
        :type mask_type: str
        :param format_re: Regular expression to be aplied in the field value before mask.
        :type format_re: str
        :param key: Key value for encrypt and decrypt algorithms
        """

        if isinstance(text,bytes):
            text = str(text.encode('utf-8'))
        else:
            text = str(text)

        if isinstance(salt,bytes):
            salt = str(salt.encode('utf-8'))
        else:
            salt = str(salt) 

        if text == "" or text == "NI" or text == "null":
            return text
        text_ori = text
        text = re.search(format_re, text).group()
        text_tmp = layout.replace("$SALT", salt)
        text = text_tmp.replace("$VALUE", text)
        if mask_type== "sha256":
            return DatamaskConfProcess.__get_hash_sha256(text)
        if mask_type == "sha512":
            return DatamaskConfProcess.__get_hash_sha512(text)
        if mask_type == "sha512/sha256":
            return DatamaskConfProcess.__get_hash_sha512_256(text)
        if mask_type in ("aes_ctr", "aes_ctru", "aes_cbc", "aes_cfb", "aes_ecb", "aes_ofb"):
            return DatamaskConfProcess.__get_aes(text_ori, key, mask_type, salt)
        if mask_type == "fte_enc":
            return DatamaskConfProcess.__get_fte_encrypt(text_ori, key, mask_type)

    @staticmethod
    def __unmask(text, salt, layout: str, mask_type: str, format_re: str, key=str):
        """__unmask.
        Unmask a text entries based on parameters

        :param text:  Text to be masked
        :param salt: Salt value to be used in before mask
        :param layout: Layout to be used to replace the salt value and the field value. $VALUE will be replaced to the field value and $SALT will be replaced to the salt value
        :type layout: str 
        :param mask_type: Type of algorithms Sha256, sha512, others
        :type mask_type: str
        :param format_re: Regular expression to be aplied in the field value before mask.
        :type format_re: str
        :param key: Key value for encrypt and decrypt algorithms
        """
        if isinstance(text, bytes):
            text = str(text.encode('utf-8'))
        else:
            text = str(text)

        if isinstance(salt, bytes):
            salt = str(salt.encode('utf-8'))
        else:
            salt = str(salt)

        if text == "" or text == "NI" or text == "null":
            return text
        text_ori = text
        text = re.search(format_re, text).group()
        text_tmp = layout.replace("$SALT", salt)
        text = text_tmp.replace("$VALUE", text)
        if mask_type in ("aes_ctr", "aes_ctru", "aes_cbc", "aes_cfb", "aes_ecb", "aes_ofb"):
            return DatamaskConfProcess.__get_daes(text_ori, key, mask_type)
        if re.search("fte_enc", mask_type) is not None :
            return DatamaskConfProcess.__get_fte_dcrypt(text_ori, key, mask_type, salt)

    def __get_mask_fiels(self):
        """__get_mask_fiels.
        :return: Mask field iter

        """
        return iter(self.__job["MaskFields"])

    def __get_domain(self, domainName: str):
        """__get_domain.

        :param domainName: Domain name to be searched
        :type domainName: str

        :return: The domain or None if it could not find
        """
        if domainName in self.__domains_idx: 
            return self.__domains[self.__domains_idx[domainName]] 
        else:
            return None

    def __get_salt(self, saltName: str):
        """__get_salt.

        :param saltName:
        :type saltName: str

        :return: The salt value or None if it could not find
        """
        if saltName in self.__salt_idx:
            return self.__salt[self.__salt_idx[saltName]]["SaltValue"] 
        else:
            return None

    def __get_df_mask_spark(self, spark, df_input): 
        """__get_df_mask_spark.
        Get the mask spark dataframe and update the all the reverse dataset if it was eanble.

        :param spark: Spark session
        :param df_input: The input spark dataframe

        :return: Spark dataframe with the mask field 
        """
        from pyspark.sql.functions import udf, lit, col
        from pyspark.sql.utils import AnalysisException
        df_mask = df_input
        sqlMask = udf(DatamaskConfProcess.__mask)
        for item in self.__get_mask_fiels():
            if item["Active"] == True:
                domain_config = self.__get_domain(item["DomainName"])
                if not domain_config:
                    raise DatamaskConfProcessError("DomainName was not found in Domains")
                salt=self.__get_salt(domain_config["SaltName"])
                if not salt:
                    raise DatamaskConfProcessError("SaltName {} does not exist in salt file".format(item["SaltName"]))

                if domain_config["MaskType"] in ("aes_ctr", "aes_ctru", "aes_cbc", "aes_cfb", "aes_ecb", "aes_ofb", "fte_enc"):
                    #Insert here the kms option. 
                    #Check if kms ARN exists, and if it does, use it as the key for encryption
                    if "EncryptKey" in domain_config and len(domain_config["EncryptKey"]) > 0:
                        encrypt_key = domain_config["EncryptKey"]
                        df_mask = df_mask.withColumn(
                            item["MaskFieldName"],
                            sqlMask(item["FieldName"],
                            lit(salt),
                            lit(domain_config["Layout"]),
                            lit(domain_config["MaskType"]),
                            lit(item["FormatRE"]), lit(domain_config["EncryptKey"])
                            )).cache()
                    else: 
                        raise DatamaskConfProcessError(
                            "EncryptKey does not exist in config file for mask type domains ")
                else:
                    df_mask = df_mask.withColumn(
                            item["MaskFieldName"], 
                            sqlMask(item["FieldName"], 
                                lit(salt), 
                                lit(domain_config["Layout"]), 
                                lit(domain_config["MaskType"]),
                                lit(item["FormatRE"])
                            ))

                if "ReverseDataset" in domain_config and domain_config["ReverseDataset"]["Active"]:
                    df_mask_reverse = df_mask.select(item["FieldName"], item["MaskFieldName"])

                    df_mask_reverse = df_mask_reverse.\
                        withColumnRenamed(item["FieldName"],domain_config["FieldAlias"]).\
                        withColumnRenamed(item["MaskFieldName"],domain_config["MaskFieldAlias"])

                    job_name_partition = False
                    if 'JobNamePartition' in domain_config['ReverseDataset'] and domain_config['ReverseDataset']['JobNamePartition']: 
                        job_name_partition = True

                    if 'JobNamePartitionFieldName' in domain_config['ReverseDataset']: 
                        job_name_partition_field_name = domain_config['ReverseDataset']['JobNamePartitionFieldName']
                    else:
                        job_name_partition_field_name = 'JobName'

                    if 'BackupDatasetPath' in domain_config['ReverseDataset']:
                        backup_path = domain_config['ReverseDataset']['BackupDatasetPath']
                    else:
                        reverse_updir = "/".join(domain_config['ReverseDataset']['DatasetPath'].split("/")[:-1])
                        reverse_dir = domain_config['ReverseDataset']['DatasetPath'].split("/")[-1]
                        backup_path = '{}/{}_bkp'.format(reverse_updir,reverse_dir) 

                    year_label = 'year'
                    month_label = 'month'
                    day_label = 'day'
                    hour_label = 'hour'
                    id_label = 'id'
                    job_label = 'job'

                    if 'BackupDatasetPartitionLabels' in domain_config['ReverseDataset']:
                        if 'Year' in domain_config['ReverseDataset']['BackupDatasetPartitionLabels']:
                            year_label = domain_config['ReverseDataset']['BackupDatasetPartitionLabels']['Year']
                        if 'Month' in domain_config['ReverseDataset']['BackupDatasetPartitionLabels']:
                            month_label = domain_config['ReverseDataset']['BackupDatasetPartitionLabels']['Month']
                        if 'Day' in domain_config['ReverseDataset']['BackupDatasetPartitionLabels']:
                            day_label = domain_config['ReverseDataset']['BackupDatasetPartitionLabels']['Day']
                        if 'Hour' in domain_config['ReverseDataset']['BackupDatasetPartitionLabels']:
                            hour_label = domain_config['ReverseDataset']['BackupDatasetPartitionLabels']['Hour']
                        if 'Id' in domain_config['ReverseDataset']['BackupDatasetPartitionLabels']:
                            id_label = domain_config['ReverseDataset']['BackupDatasetPartitionLabels']['Id']

                    year=datetime.datetime.now().year
                    month=datetime.datetime.now().month
                    day=datetime.datetime.now().day
                    hour=datetime.datetime.now().hour
                    id_uuid=str(uuid.uuid4())
                    job=self.__job["JobName"]

                    partition_backup='{}={}/{}={}/{}={}/{}={}/{}={}/{}={}'.format(\
                            year_label, year, \
                            month_label, month, \
                            day_label, day, \
                            hour_label, hour, \
                            job_label, job,  \
                            id_label, id_uuid)

                    backup_full_path = '{}/{}'.format(backup_path, partition_backup)

                    #df_all_dedup_reverse = df_reverse_dataset.where(df_reverse_dataset.MaskTableReference == table_path).union(df_mask_reverse).dropDuplicates()
                   
                    df_mask_reverse.dropDuplicates()

                    if 'BackupCoalesce' in domain_config['ReverseDataset']:
                        df_mask_reverse = df_mask_reverse.coalesce(domain_config['ReverseDataset']['BackupCoalesce']) 

                    df_mask_reverse\
                            .write\
                            .format("parquet")\
                            .option("compression", "snappy")\
                            .option("path", backup_full_path)\
                            .mode("append")\
                            .save()
                   
                    if not 'KeepOnlyBackp' in domain_config['ReverseDataset'] or not domain_config['ReverseDataset']['KeepOnlyBackp']:
                        df_backup = spark.read.parquet(backup_full_path)

                        if job_name_partition:
                            df_backup = df_backup.select(domain_config["FieldAlias"], domain_config["MaskFieldAlias"]).withColumn(job_name_partition_field_name,lit(job))
                            df_backup.schema[job_name_partition_field_name].nullable = True
                            df_mask_reverse = df_mask_reverse.withColumn(job_name_partition_field_name,lit(job))
                            df_mask_reverse.schema[job_name_partition_field_name].nullable = True
                        else:
                            df_backup = df_backup.select(domain_config["FieldAlias"], domain_config["MaskFieldAlias"])

                        schema=df_mask_reverse.schema
                        path_exists=True
    
                        try:
                            df_reverse_dataset = spark.read.parquet(domain_config['ReverseDataset']['DatasetPath']) 
                        except AnalysisException as e:
                            _logger.warning("Infering that is the first load in this table partition log path, directory does not exists")
                            df_reverse_dataset = spark.createDataFrame([],schema)
                            path_exists=False
    
                        _logger.info("df_mask_reerse.schema:## {}  ##".format(df_mask_reverse.schema))
                        _logger.info("df_reverse_dataset.schema:## {}  ##".format(df_reverse_dataset.schema))

                        if path_exists and df_mask_reverse.schema != df_reverse_dataset.schema:
                            raise DatamaskConfProcessError("The new Reverse Dataset has diferent schema than the Reverse Dataset in storage, please delete or migrate the currently Reverse Dataset in storage to the new version of Datamask Framework")

                        _logger.info("df_mask_reverse.schema:## {}##".format(df_mask_reverse.schema))
                        _logger.info("df_reverse_dataset.schema:## {}##".format(df_reverse_dataset.schema))

                        if job_name_partition:
                            spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic")
                            df_reverse_dataset = df_reverse_dataset.filter(col(job_name_partition_field_name) == lit(job))
                        else:
                            spark.conf.set("spark.sql.sources.partitionOverwriteMode","static")

                        df_union = df_backup.union(df_mask_reverse).dropDuplicates()

                        write_stm = df_union\
                                .coalesce(domain_config['ReverseDataset']['Coalesce'])\
                                .write\
                                .format("parquet")\
                                .option("compression", "snappy")\
                                .option("path", domain_config['ReverseDataset']['DatasetPath'])\
                                .mode("overwrite")\

                        if job_name_partition:
                            write_stm.partitionBy(job_name_partition_field_name)
                
                        if "ReverseTable" in domain_config['ReverseDataset']\
                                and "ReverseDatabase" in domain_config['ReverseDataset']:
                            write_stm.saveAsTable('{}.{}'.format(domain_config['ReverseDataset']["ReverseDatabase"], domain_config['ReverseDataset']["ReverseTable"]))
                        else:
                            write_stm.save()
                else:
                    _logger.warning("ReverseDataset is not enable")
                df_mask = df_mask.drop(item["FieldName"])
                if not ("KeepMaskName" in item and item["KeepMaskName"]):
                    df_mask = df_mask.withColumnRenamed(item["MaskFieldName"],item["FieldName"])
        return df_mask         

    def __filter_partitions_spark (self, df_input, part_list: list):
        """__filter_partitions_spark.
        Filter partitions in a spark dataframe

        :param df_input: Spark dataframe input
        :param part_list: Partitions key list
        :type part_list: list

        :return: Filtered spark dataframe

        """
        where_clause = self.__get_where_clause_from_hive_part_list(part_list)
        return df_input.where(where_clause)

    def __write_output_spark (self, spark,df_input):
        """__write_output_spark.
        Write the output dataset baseed on the properties

        :param df_input: Spark Dataframe input
        """

        if len(self.__partition_keys) > 0:
            spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic")
        else:
            spark.conf.set("spark.sql.sources.partitionOverwriteMode","static")

        write_stm = df_input.coalesce(self.__job["Output"]["Coalesce"]). write\
            .format("parquet")\
            .option("compression", "snappy")\
            .option("path", self.__job["Output"]["OutputPath"])\
            .mode("overwrite")

        if len(self.__partition_keys) > 0:
            write_stm.partitionBy(*self.__partition_keys)

        if "OutputTable" in self.__job["Output"]\
                and self.__job["Output"]["OutputTable"] \
                and "OutputDatabase" in self.__job["Output"] \
                and self.__job["Output"]["OutputDatabase"]:
            write_stm.saveAsTable('{}.{}'.format(self.__job["Output"]["OutputDatabase"], self.__job["Output"]["OutputTable"]))
        else:
            write_stm.save()

        return

    def process_spark(self, part_list: list, spark):
        """process_spark.
        Process the data mask pipeline with spark

        :param part_list: Partition Key list to be filtered
        :type part_list: list
        :param spark: Spark Session 
        """

        if "PartitionColumnTypeInference" in self.__job['Input'] and not self.__job['Input']['PartitionColumnTypeInference']:
            spark.conf.set("spark.sql.sources.partitionColumnTypeInference.enabled","false")

        input_path = self.__get_input_path()
        input_path_type = "s3"
        
        # Check FileSystem and if exists files in path
        if input_path.find("s3") == -1:
            input_path_type = 'local'
            if not exists_files_local(input_path):
                return
        else:
            if not exists_files_s3(input_path):
                return
        
        df_input = self.__read_input_spark(spark)

        df_filtered = df_input

        if len(part_list) > 0:
            df_filtered = self.__filter_partitions_spark(df_filtered, part_list)

        df_mask = self.__get_df_mask_spark(spark, df_filtered) 

        self.__write_output_spark(spark, df_mask)

        # Delete Landing if needed
        if self.__get_input_delete(): 
            if len(part_list) > 0:
                for part in part_list:
                    if input_path_type == 'local':
                        delete_path_local("{}/{}".format(input_path, part))
                    else:
                        delete_path_s3("{}/{}".format(input_path, part))
            else:
                if input_path_type == 'local':
                    delete_path_local(input_path)
                else:
                    delete_path_s3(input_path)

        return
    
    def process_pandas(self, part_list: list):
        """process_pandas.
        Process the data mask pipeline with pandas

        :param part_list:
        :type part_list: list
        """
        pass
        return

    def process_spark_streaming(self, topic_list: list):
        """process_spark_streaming.
        Start the streaming processing to mask a stream

        :param topic_list:
        :type topic_list: list
        """
        pass
        return



      


        
        









