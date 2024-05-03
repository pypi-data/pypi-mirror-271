import pytest

from xl2thrift import convertXlsxToThrift
from xl2thrift import EnumException, ThriftGeneratedModuleException, FileNotFoundException

# def testArgGenPy():
#     namespace = "BadEnergy.Config"
#     thrift_protocol = "TJSONProtocol"
#     gen_py = "tests/does-not-exist"
#     class_name = "Data"
#     output = "tests/config.bin"
#     enums_path = "tests/Excel/enums.txt"
#     release = False
#     with pytest.raises(ThriftGeneratedModuleException):
#         convertXlsxToThrift("tests/ExcelCases/BasicallyEmpty.xlsx", namespace=namespace, thrift_protocol=thrift_protocol, gen_py=gen_py, class_name=class_name, output=output, enums_path=enums_path, release=release)

def testBadEnum():
    namespace = "BadEnergy.Config"
    thrift_protocol = "TJSONProtocol"
    gen_py = "tests/gen-py"
    class_name = "Data"
    output = "tests/config.bin"
    enums_path = "tests/Excel/enums.txt"
    release = False
    with pytest.raises(EnumException, match='.*[eE]num.*'):
        convertXlsxToThrift("tests/ExcelCases/BadEnum.xlsx", namespace=namespace, thrift_protocol=thrift_protocol, gen_py=gen_py, class_name=class_name, output=output, enums_path=enums_path, release=release)

def testMissingEnumsList():
    namespace = "BadEnergy.Config"
    thrift_protocol = "TJSONProtocol"
    gen_py = "tests/gen-py"
    class_name = "Data"
    output = "tests/config.bin"
    enums_path = "tests/Excel/does-not-exist.txt"
    release = False
    with pytest.raises(FileNotFoundException, match='.*[eE]num.*'):
        convertXlsxToThrift("tests/ExcelCases/BasicallyEmpty.xlsx", namespace=namespace, thrift_protocol=thrift_protocol, gen_py=gen_py, class_name=class_name, output=output, enums_path=enums_path, release=release)

def testArgClassName():
    namespace = "BadEnergy.Config"
    thrift_protocol = "TJSONProtocol"
    gen_py = "tests/gen-py"
    class_name = "SomeUndefinedClass"
    output = "tests/config.bin"
    enums_path = "tests/Excel/enums.txt"
    release = False
    with pytest.raises(FileNotFoundException, match='.*class.*'):
        convertXlsxToThrift("tests/ExcelCases/BasicallyEmpty.xlsx", namespace=namespace, thrift_protocol=thrift_protocol, gen_py=gen_py, class_name=class_name, output=output, enums_path=enums_path, release=release)
