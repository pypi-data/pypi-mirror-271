import argparse

from .thriftExcelTools import convertXlsxToThrift

def convertXlsx():

	parser = argparse.ArgumentParser(description='Excel converter')
	parser.add_argument('patterns', nargs='*', default="*.xlsx", help='list of files, folders and globs')
	parser.add_argument('--namespace', help='namespace from thrift file', required=True)
	parser.add_argument('--thrift_protocol', choices=('TCompactProtocol', 'TJSONProtocol', 'TBinaryProtocol'), default='TJSONProtocol', required=True)
	parser.add_argument('--gen_py', default='', help="location of thrift-generated python source folder (thrift --gen py <thriftfile>)", required=True)
	parser.add_argument('--output', default='config.bin', required=False, help="where to save output")
	parser.add_argument('--class_name', default='Data', help="name of the class (without namespace) in your thrift file that contains all the data")
	parser.add_argument('--verbose', action='store_true', help="show detailed output")
	parser.add_argument('--enums', help="name of text file that stores a list of enums (coming soon)")
	parser.add_argument('--release', action='store_true', help='do not process folders ending with Debug')

	try:
		args = parser.parse_args()
		globals()['verbose'] = args.verbose
		print("verbose %s" % (globals()['verbose']))
	except IOError as msg:
		parser.error(str(msg))
		usage()

	gen_py = args.gen_py
	namespace = args.namespace
	class_name = args.class_name
	enums_path = args.enums
	print('enums_path %s' % (enums_path))
	release = args.release
	thrift_protocol = args.thrift_protocol
	output = args.output
	return convertXlsxToThrift(args.patterns, namespace=namespace, thrift_protocol=thrift_protocol, gen_py=gen_py, class_name=class_name, output=output, enums_path=enums_path, release=release, verbose=args.verbose)

def main():
    convertXlsx()

# if __name__ == '__main__':
#     convertXlsx()
