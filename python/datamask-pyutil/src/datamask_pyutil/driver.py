import sys
import importlib
import argparse
from pkg_resources import get_distribution, DistributionNotFound

module = importlib.import_module('datamask_pyutil.pyspark')
#sys.exit(module.main(sys.argv))
module.main(sys.argv)
