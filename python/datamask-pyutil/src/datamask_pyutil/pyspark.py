# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function
#from pyspark.sql.functions import date_format, max as max_, lit, from_json, udf,  col, decode, concat, regexp_replace, current_timestamp
from pyspark.sql.functions import substring, concat, split, size, lit, sha2, udf
from pyspark.sql.types import StringType, StructType, StructField, Row
from pyspark.sql.utils import AnalysisException
from pyspark.context import SparkContext

import sys
from random import random
from operator import add

from pyspark.sql import SparkSession
import re 
import hashlib

import argparse
import sys
import json
import logging

from datamask_pyutil.utility import setup_logging
import datamask_pyutil.conf_process  as conf_process

from datamask_pyutil import __version__

__author__ = "Diogo Kato"
__copyright__ = "Diogo Kato"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class DatamaskPysparkError(Exception):
    pass

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Sql4spark is a pyspark module to execute SQL on spark and merge data with output")
    parser.add_argument(
        "--part-list",
        dest="partList",
        required=False,
        help="Partitions list, Comma ',' delimited",
        metavar="STRING")
    parser.add_argument(
        "--config-path",
        required=True,
        dest="configPath",
        help="Config Path",
        metavar="STRING")
    parser.add_argument(
        "--is-glue-job",
        required=False,
        default=False,
        dest="isGlueJob",
        help="Is a Glue Job?",
        action="store_true")
    parser.add_argument(
        "--disable-glue-catalog",
        required=False,
        default=False,
        dest="disableGlueCatalog",
        help="Glue catalog",
        action="store_true")
    parser.add_argument(
        "--job-name",
        required=True,
        dest="jobName",
        help="Job name in the config json",
        metavar="STRING")
    parser.add_argument(
        "--version",
        action="version",
        version="datamask-pyutil {ver}".format(ver=__version__))
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="Set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="Set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_known_args(args)

def exit_error(spark, message, code):
    _logger.error(message)
    raise DatamaskPysparkError(message)

def main(argsv):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args, unknown_args = parse_args(argsv)

    setup_logging(args.loglevel)

    _logger.info("###################################")
    _logger.info("###################################")
    _logger.info("Unknow Parameters")
    _logger.info("{}".format(unknown_args))
    _logger.info("###################################")
    _logger.info("###################################")

    _logger.debug("Starting datamsk-pyutil-pyspark")
    if args.isGlueJob:
        from awsglue.utils import getResolvedOptions
        from awsglue.context import GlueContext
        from awsglue.job import Job
        args_glue = getResolvedOptions(argsv, ['JOB_NAME'])
        sc = SparkContext()
        glueContext = GlueContext(sc)
        spark = glueContext.spark_session
        job = Job(glueContext)
        job.init(args_glue['JOB_NAME'], args_glue)
    else:
        if args.disableGlueCatalog:
            spark = SparkSession.builder.appName("datamask-pyutil-{}".format(args.jobName)).enableHiveSupport().getOrCreate()
        else:
            spark = SparkSession.builder.appName("datamask-pyutil-{}".format(args.jobName)).config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory").enableHiveSupport().getOrCreate()


    _logger.info("Initialize datamask-pyutil")
    _logger.info("###################################")
    _logger.info("")
    _logger.info("spark: {}".format(spark))
    _logger.info("partList: {}".format(args.partList))
    _logger.info("configPath: {}".format(args.configPath))
    _logger.info("jobName: {}".format(args.jobName))
    _logger.info("isGlueJob: {}".format(args.isGlueJob))
    _logger.info("disableGlueCatalog: {}".format(args.disableGlueCatalog))
    _logger.info("")
    _logger.info("###################################")

    _logger.info("Getting Json Conf")
    cf = conf_process.DatamaskConfProcess(args.configPath, args.jobName)
        
    if not cf.is_job_active():
        exit_error(spark,"Jobname[{}] is not active".format(args.jobName))

    part_vet = []
    if args.partList and args.partList != '':
        part_vet = args.partList.split(",")

    cf.process_spark(part_vet, spark)

    spark.stop() 

    _logger.info("Script ends here")

def run():
    """Entry point for console_scripts
    """
    main(sys.argv)


if __name__ == "__main__":
    run()
