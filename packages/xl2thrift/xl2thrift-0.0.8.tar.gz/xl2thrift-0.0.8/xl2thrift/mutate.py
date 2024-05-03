import sys, os
import importlib
import thrift
from thrift.transport import TTransport
from thrift.Thrift import TType

from .exceptions import EnumException, ThriftGeneratedModuleException, FileNotFoundException

def Log(s):
	verbose = globals()['verbose']
	if verbose:
	 	print(s)

def load_modules(folder_path):
    module_names = []
    modules = []

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out files that are not Python modules
    python_files = [file for file in files if file.endswith('.py')]

    # Remove file extension from module names
    module_names = [file[:-3] for file in python_files]

    # Import modules dynamically
    for name in module_names:
        print(name)
        spec = importlib.util.spec_from_file_location(name, os.path.join(folder_path, name + '.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append(module)

    return modules

def mutate(mutators_folder, gen_py, namespace, class_name='Data', inputPath='config.bin', outputPath='config.bin', thrift_protocol='TJSONProtocol', verbose=True):

    globals()['verbose'] = verbose

    sys.path.append(gen_py)
    ConfigModule = {}
    try:
        ConfigModule = importlib.import_module('%s.ttypes' % (namespace))
    except:
        print('Failed to load thrift-generated module (%s.ttypes)' % (namespace))
        print('Check that the namespace in your thrift file matches the --namespace arg (%s)' % (namespace))
        print('and that the --gen_py arg (%s) points to the correct folder' % (gen_py))
        raise ThriftGeneratedModuleException('Failed to load thrift-generated module in <%s> called (%s.ttypes)' % (gen_py, namespace))
    finally:
        sys.path.remove(gen_py)

    globals()['ConfigModule'] = ConfigModule

    try:
        dataClass = getattr(ConfigModule, class_name)
    except:
        print('Please make sure that your --class_name arg refers to the correct class in your thrift file (and in the source code in --gen_py)')
        raise FileNotFoundException('Failed create an instance of class (%s) specified in the --class_name arg' % (class_name))

    with open(inputPath, 'rb') as f:
        buf = f.read()
        f.close()

    transport = TTransport.TMemoryBuffer(buf)
    ThriftProtocol = getattr(importlib.import_module("thrift.protocol.%s" % (thrift_protocol)), thrift_protocol)
    protocol = ThriftProtocol(transport)
    Data = dataClass()
    Data.read(protocol)
    globals()['Data'] = dataClass()

    modules = load_modules(mutators_folder)
    for module in modules:
        if '__mutators' in dir(module):
            # mutator_names = module.__mutators
            for mutator_function in module.__mutators:
                mutator_function(Data)

    transport = TTransport.TMemoryBuffer()
    protocol = ThriftProtocol(transport)
    Data.write(protocol)
    buf = transport.getvalue()
    with open(outputPath, 'wb') as f:
        f.write(buf)
        f.close()


