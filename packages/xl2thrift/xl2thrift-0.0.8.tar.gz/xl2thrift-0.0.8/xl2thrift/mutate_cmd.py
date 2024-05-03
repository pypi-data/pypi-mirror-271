import sys, os
import importlib
import argparse

import thrift
from thrift.transport import TTransport
from thrift.Thrift import TType

from .mutate import mutate
from .exceptions import EnumException, ThriftGeneratedModuleException, FileNotFoundException

def Log(s):
	verbose = globals()['verbose']
	if verbose:
	 	print(s)

def mutateThriftBlob():
    parser = argparse.ArgumentParser(description='Executes user-defined mutator methods on an xl2thrift blob file')
    parser.add_argument('--mutators_folder', help='folder that contains mutators', required=True)
    parser.add_argument('--gen_py', default='', help="location of thrift-generated python source folder (thrift --gen py <thriftfile>)", required=True)
    parser.add_argument('--namespace', help='namespace from thrift file', required=True)
    parser.add_argument('--class_name', default='Data', help="name of the class (without namespace) in your thrift file that contains all the data")
    parser.add_argument('--input_path', default='config.bin', required=False, help="input blob")
    parser.add_argument('--output_path', default='config.bin', required=False, help="output blob")
    parser.add_argument('--thrift_protocol', choices=('TCompactProtocol', 'TJSONProtocol', 'TBinaryProtocol'), default='TJSONProtocol', required=True)
    parser.add_argument('--verbose', action='store_true', help="show detailed output")

    try:
        args = parser.parse_args()
        globals()['verbose'] = args.verbose
    except IOError as msg:
        parser.error(str(msg))
        mutateUsage()

    mutate(mutators_folder=args.mutators_folder,
            gen_py=args.gen_py,
            namespace=args.namespace,
            class_name=args.class_name,
            inputPath=args.input_path,
            outputPath=args.output_path,
            thrift_protocol=args.thrift_protocol,
            verbose=args.verbose
            )
