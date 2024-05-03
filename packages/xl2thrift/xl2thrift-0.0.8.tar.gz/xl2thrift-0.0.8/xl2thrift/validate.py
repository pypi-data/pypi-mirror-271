import sys, os, os.path
import importlib
import thrift
from thrift.transport import TTransport
from thrift.Thrift import TType
import argparse
import traceback

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

errors = []
warnings = []
assetPaths = []
prefabAssetFileExtensions = []
audioAssetFileExtensions = []
imageAssetFileExtensions = []
assetMetaFileExtensions = []

def Log(s):
	if verbose:
		print(s)

# try:
# 	args = parser.parse_args()
# 	Log('namespace: %s' % args.namespace)
# except IOError as msg:
#     parser.error(str(msg))

# sys.path.append('../Thrift/%s/gen-py' % args.config_subfolder)
# ConfigModule = importlib.import_module('%s.ttypes' % (args.namespace))
# ThriftConstants = importlib.import_module('%s.constants' % (args.namespace))

def AddError(errorMessage):
	global errors
	print(errorMessage)
	errors.append(errorMessage)

def AddWarning(message):
	global warnings
	print(message)
	warnings.append(message)

# this is annoying. i could not figure out how to make this a static method in class __Check
# it doesn't seem like a static method can call another static method of the same class
def AssetExists(relativePath, assetFileExtensions, errorMessage):
	# Kludge - if no assets paths then don't validate assets. But that means returning true here
	if not assetPaths:
		return True

	filename, ext = os.path.splitext(relativePath)
	if ext != '':
		for folderPath in assetPaths:
			path = folderPath + relativePath
			if os.path.exists(path):
				return True
		return False

	found = False
	for folderPath in assetPaths:
		for assetFileExtension in assetFileExtensions:
			path = folderPath + relativePath + assetFileExtension
			if os.path.exists(path):
				return True

	return False

def AssetExistsWithExtension(relativePath, errorMessage):
	# If no assets paths then don't validate assets
	if not assetPaths:
		return True

	found = False
	for folderPath in assetPaths:
		path = folderPath + relativePath
		if os.path.exists(path):
			return True
	return False

def AssetMetaFileExists(relativePath, assetFileExtensions, assetMetaFileExtensions, errorMessage):
	# If no assets paths then don't validate assets
	if not assetPaths:
		return True

	filename, ext = os.path.splitext(relativePath)
	if ext != '':
		for folderPath in assetPaths:
			for assetMetaFileExtension in assetMetaFileExtensions:
				path = folderPath + relativePath + assetMetaFileExtension
				if os.path.exists(path):
					return True
		return False

	found = False
	for folderPath in assetPaths:
		for assetFileExtension in assetFileExtensions:
			path = folderPath + relativePath + assetFileExtension
			for assetMetaFileExtension in assetMetaFileExtensions:
				path = path + assetMetaFileExtension
				if os.path.exists(path):
					return True
	return False

class __Check:
	@staticmethod
	def IsTrue(testvalue, errorMessage):
		if testvalue == False:
			AddError(errorMessage)
	@staticmethod
	def IsFalse(testvalue, errorMessage):
		if testvalue == True:
			AddError(errorMessage)

	@staticmethod
	def Exists(testvalue, errorMessage):
		if testvalue == None:
			AddError(errorMessage)

	@staticmethod
	def SoundExists(soundId, errorMessage):
		Data = globals()['Data']
		if not soundId in Data.soundClips and not soundId in Data.soundClipLists:
			print(('Missing sound clip or sound clip list (%s): %s' % (errorMessage, soundId)))
	@staticmethod
	def AudioAssetExists(relativePath, errorMessage):
		if relativePath != None and not AssetExists(relativePath, audioAssetFileExtensions, errorMessage):
			AddError(errorMessage)
		if not AssetMetaFileExists(relativePath, audioAssetFileExtensions, assetMetaFileExtensions, errorMessage):
			print(('Missing audio asset meta file (%s): %s' % (errorMessage, relativePath)))
	@staticmethod
	def PrefabAssetExists(relativePath, errorMessage):
		if not assetPaths:
			return True
		if relativePath != None:
			global numerrors
# 			if not relativePath.endswith('.prefab'):
# 				AddWarning('Prefab asset path must end with .prefab: %s' % (relativePath))
			# TODO: clean up
			if relativePath.endswith('.prefab'):
				assetExists = AssetExistsWithExtension(relativePath, errorMessage)
			else:
				assetExists = AssetExists(relativePath, prefabAssetFileExtensions, errorMessage)
			if not assetExists:
				AddError('Missing prefab asset (%s): %s' % (errorMessage, relativePath))
	@staticmethod
	# use this local version when the config path includes the extension
	def AssetExists(relativePath, errorMessage):
		if relativePath == None:
			return True
		if not assetPaths:
			return True
		for folderPath in assetPaths:
			path = folderPath + relativePath
			if os.path.exists(path):
				return True
				break
		AddError('Missing (literal) asset (%s): %s' % (errorMessage, relativePath))
	@staticmethod
	def ImageAssetExists(relativePath, errorMessage):
		if relativePath != None and not AssetExists(relativePath, imageAssetFileExtensions, errorMessage):
			AddError('Missing image asset (%s): %s' % (errorMessage, relativePath))
		elif not AssetMetaFileExists(relativePath, imageAssetFileExtensions, assetMetaFileExtensions, errorMessage):
			print(('Missing image asset meta file (%s): %s' % (errorMessage, relativePath)))
	@staticmethod
	def IsValidString(s, errorMessage):
		if s == None or s == "":
			AddError('IsValidString: %s' % (s))
			traceback.print_stack()
	@staticmethod
	def IsNotValidString(s, errorMessage):
		if s != None and s != "":
			AddError('IsNotValidString: %s' % (s))
			traceback.print_stack()
	@staticmethod
	def Contains(dic, key, errorMessage):
		if not key in dic:
			AddError('key <%s> not found: %s ' % (key, errorMessage))
	@staticmethod
	def NotEmptyDictionary(dic, errorMessage):
		if dic == None or not any(dic):
			AddError(s)
	@staticmethod
	def NotEmptyList(list, errorMessage):
		if list == None or not list:
			AddError(s)
	@staticmethod
	def ListsAreSameLength(testvalue1, testvalue2, errorMessage):
		if (testvalue1 == None and testvalue2 != None) or (testvalue1 != None and testvalue2 == None) or ((testvalue1 != None) and (len(testvalue1) != len(testvalue2))):
			global numerrors
			AddError(s)
	@staticmethod
	def AllItemsInListExistInTable(thelist, thetable, errorMessage):
		if thelist != None:
			for v in thelist:
				if thetable == None or not v in thetable:
					AddError(s)
	@staticmethod
	def NotEmpty(listordic, errorMessage):
		global numerrors
		global errors
		if listordic == None:
			AddError(('ERROR: %s' % (errorMessage)))
		if type(listordic) == type([]):
			if list == None or not list:
				AddError(errorMessage)
		else:
			if listordic == None or not any(listordic):
				AddError(errorMessage)

class __Warn:
	@staticmethod
	def IsTrue(testvalue, warningMessage):
		if testvalue == False:
			AddWarning(warningMessage)

	@staticmethod
	def Exists(testvalue, warningMessage):
		if testvalue == None:
			AddWarning(warningMessage)

def addAssetFolder(path):
	Log('addAssetFolder: <%s>' % (path))
	assetPaths.append(path)

def addPrefabAssetFileExtension(fileExtension):
	Log('Add Prefab Asset File Extension: <%s>' % (fileExtension))
	prefabAssetFileExtensions.append(fileExtension)

def addAudioAssetFileExtension(fileExtension):
	Log('Add Audio Asset File Extension: <%s>' % (fileExtension))
	audioAssetFileExtensions.append(fileExtension)

def addImageAssetFileExtension(fileExtension):
	Log('Add Image Asset File Extension: <%s>' % (fileExtension))
	imageAssetFileExtensions.append(fileExtension)

def addAssetMetaFileExtension(fileExtension):
	Log('Add Asset Meta File Extension: <%s>' % (fileExtension))
	assetMetaFileExtensions.append(fileExtension)

def validate(validators_folder, asset_paths, gen_py, namespace, class_name, input_path, thrift_protocol, verbose):

	globals()['verbose'] = verbose

	addPrefabAssetFileExtension('.prefab')
	addAudioAssetFileExtension('.wav')
	addAudioAssetFileExtension('.aif')
	addAudioAssetFileExtension('.ogg')
	addImageAssetFileExtension('.png')
	addAssetMetaFileExtension('.meta')
	if asset_paths:
		paths = asset_paths.split(',')
		for path in paths:
			addAssetFolder(path)

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

	try:
		dataClass = getattr(ConfigModule, class_name)
	except:
		print('Please make sure that your --class_name arg refers to the correct class in your thrift file (and in the source code in --gen_py)')
		raise FileNotFoundException('Failed create an instance of class (%s) specified in the --class_name arg' % (class_name))

	with open(input_path, 'rb') as f:
		buf = f.read()
		f.close()

	transport = TTransport.TMemoryBuffer(buf)
	ThriftProtocol = getattr(importlib.import_module("thrift.protocol.%s" % (thrift_protocol)), thrift_protocol)
	protocol = ThriftProtocol(transport)
	# Data = ConfigModule.Data()
	Data = dataClass()
	Data.read(protocol)

	globals()['Data'] = Data
	# allow validators to import validate.ConfigModule
	globals()['ConfigModule'] = ConfigModule

	modules = load_modules(validators_folder)
	for module in modules:
		if '__validators' in dir(module):
			# mutator_names = module.__mutators
			for validator_function in module.__validators:
				validator_function(Data)

	# sys.path.append(validators_folder)
	# ValidatorModule = importlib.import_module(validators_folder)
	# sys.path.remove(validators_folder)
	# #print dir(ValidatorModule)
	# for modulename in dir (ValidatorModule):
	# 	if modulename[:2] != "__":
	# 		#print("modulename " + modulename)
	# 		module = getattr(ValidatorModule, modulename)
	# 		if '__validators' in dir(module):
	# 			for function in module.__validators:
	# 				function(data)

	# if warnings != []:
	# 	print(("Validate (%s): There were %d warnings" % (validators_folder, len(warnings))))
	# 	print('WARNINGS SUMMARY:')
	# for warning in warnings:
	# 	print(('WARNING: %s' % (warning)))
	# if errors != []:
	# 	print('ERRORS SUMMARY:')
	# 	for error in errors:
	# 		print(('ERROR: %s' % (error)))
		# exit("Validate (%s): There were %d errors" % (validators_folder, len(errors)))
	return [warnings, errors]

# Begin


# config_subfolder = args.config_subfolder
# if config_subfolder != '':
# 	if not config_subfolder.endswith('/'):
# 		config_subfolder += '/'


# if not assetPaths:
# 	print('Warning: no asset paths specified. Will not validate assets')

# validate(Data)
