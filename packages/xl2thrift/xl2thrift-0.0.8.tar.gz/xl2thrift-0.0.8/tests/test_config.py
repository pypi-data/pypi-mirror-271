import sys
import importlib
import subprocess

import pytest
import thrift
from thrift.transport import TTransport
from thrift.Thrift import TType

from xl2thrift import convertXlsxToThrift
from xl2thrift import usage
from xl2thrift import exceptions

def test_convert():
    namespace = "BadEnergy.Config"
    thrift_protocol = "TJSONProtocol"
    gen_py = "tests/gen-py"
    class_name = "Data"
    output = "tests/config.bin"
    enums_path = "tests/Excel/enums.txt"
    release = False

    convertXlsxToThrift("tests/Excel/*.xlsx", namespace=namespace, thrift_protocol=thrift_protocol, gen_py=gen_py, class_name=class_name, output=output, enums_path=enums_path, release=release, verbose=True)
    # subprocess.call(['xl2thrift', 'tests/Excel/**.xlsx', '--namespace %s' % (namespace), '--thrift_protocol %s' % (thrift_protocol), '--gen_py %s' % (gen_py), '--class_name %s' % (class_name), '--output %s' % (output), '--enums_path %s' % (enums_path), '--verbose']) 
    # xl2thrift tests/Excel/*.xlsx --namespace BadEnergy.Config --thrift_protocol TJSONProtocol --gen_py tests/gen-py --output tests/config.bin --class_name Data --enums tests/Excel/enums.txt  

    # Load classes
    ConfigModule = {}
    try:
        sys.path.append('%s' % (gen_py))
        ConfigModule = importlib.import_module('%s.ttypes' % (namespace))
    except:
        pytest.fail('Failed to import thrift-generated module (%s.ttypes) from path <%s>' % (namespace, gen_py))
    finally:
        sys.path.remove('%s' % (gen_py))

    try:
        dataClass = getattr(ConfigModule, class_name)
    except:
        pytest.fail('Failed create an instance of class (%s) specified in the class_name arg' % (class_name))

    # Load output file
    with open(output, 'rb') as f:
        buf = f.read()
        f.close()
    assert(buf != None)

    transport = TTransport.TMemoryBuffer(buf)
    thriftProtocol = getattr(importlib.import_module("thrift.protocol.%s" % (thrift_protocol)), thrift_protocol)
    assert(thriftProtocol != None)
    protocol = thriftProtocol(transport)
    assert(protocol != None)
    Data = dataClass()
    if Data == None:
        pytest.fail("Failed to instantiate data_class")
    Data.read(protocol)

    # Check loaded data for correctness

    # Map
    assert(Data.purchaseOffers != None)
    assert(Data.purchaseOffers["Epic Hero"] != None)
    assert(Data.purchaseOffers["Epic Hero"].shopItemPrefab == "Assets/Data/UI/Shop/ShopHeroBigItem.prefab")

    # Enum
    affinityClass = getattr(ConfigModule, "AffinityID")
    assert(Data.heroSummons != None)
    assert(Data.heroSummons["Multi Yellow Hero"] != None)
    assert(Data.heroSummons["Multi Yellow Hero"].affinityId == affinityClass.Yellow)
    
    # Struct
    assert(Data.guildSettings != None)
    assert(Data.guildSettings.guildLeaderSectionId == "guild-mlist-info-leader-section-default")

    # Bool table
    assert(Data.boolTable != None)
    assert(Data.boolTable["Minigame.DebugButtons.Enable"] == False) 

    # String table - requires mutators
    # assert(Data.text.editGuildSelectIcon == "Select avatar")

    # List of strings in cell
    assert(len(Data.hudProfiles["BattleMenuRaidMode"].currencyIds) == 3)

    # List if int in cell
    assert(Data.strengthProfiles["Rare Pierce"].inflectDamage[2] == 400)

