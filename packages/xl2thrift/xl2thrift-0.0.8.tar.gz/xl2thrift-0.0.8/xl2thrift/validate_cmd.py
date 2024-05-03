import sys, os
import importlib
import argparse

import thrift
from thrift.transport import TTransport
from thrift.Thrift import TType

from .valdate import validate
from .exceptions import EnumException, ThriftGeneratedModuleException, FileNotFoundException

def Log(s):
	verbose = globals()['verbose']
	if verbose:
	 	print(s)

def validateThriftBlob():
    parser = argparse.ArgumentParser(description='Executes user-defined mutator methods on an xl2thrift blob file')
    parser.add_argument('--validators_folder', help='folder that contains validators', required=True)
    parser.add_argument('--asset_folders', help='list of folders that contains assets', required=False)
    parser.add_argument('--gen_py', default='', help="location of thrift-generated python source folder (thrift --gen py <thriftfile>)", required=True)
    parser.add_argument('--namespace', help='namespace from thrift file', required=True)
    parser.add_argument('--class_name', default='Data', help="name of the class (without namespace) in your thrift file that contains all the data")
    parser.add_argument('--input_path', default='config.bin', required=False, help="input blob")
    parser.add_argument('--thrift_protocol', choices=('TCompactProtocol', 'TJSONProtocol', 'TBinaryProtocol'), default='TJSONProtocol', required=True)
    parser.add_argument('--verbose', action='store_true', help="show detailed output")

    try:
        args = parser.parse_args()
        globals()['verbose'] = args.verbose
    except IOError as msg:
        parser.error(str(msg))
        validateUsage()

    validate(validators_folder=args.validators_folder,
            asset_paths=args.asset_paths,
            gen_py=args.gen_py,
            namespace=args.namespace,
            class_name=args.class_name,
            inputPath=args.input_path,
            thrift_protocol=args.thrift_protocol,
            verbose=args.verbose
            )
