import os
import json
import yaml

def WriteDictJson(outdict, path):

    jsonStr = json.dumps(outdict, indent=2, sort_keys=False)
    with open(path,"w") as f:
        f.write(jsonStr)
    return True

def ReadDictJson(filepath):
    jsondict = None
    try:
        with open(filepath) as json_file:
            jsondict = json.load(json_file)
        if not jsondict:
            print('Failed to load {}'.format(filepath))
    except Exception as err:
        print("Exception {}: ReadDictJson failed to load {}.  {}".format(type(err), filepath, err))
        raise err
    return jsondict

def Dict2Json(outdict):
    jsonStr = json.dumps(outdict, sort_keys=False, indent=4)      
    return jsonStr

def Json2Dict(json_file):
    jsondict = json.load(json_file)
    return jsondict

def ReadDictYaml(filepath):
    yamldict = {}
    try:
        with open(filepath) as yaml_file:
            yamldict = yaml.safe_load(yaml_file)
        if not yamldict:
            print('Failed to load {}'.format(filepath))
    except Exception as err:
        print("Exception {}: ReadDictYaml failed to load {}.  {}".format(type(err), filepath, err))
        raise err
    return yamldict

def WriteDictYaml(outdict, path):
    yamlStr = yaml.dump(outdict, indent=2, sort_keys=False)
    with open(path,"w") as f:
        f.write(yamlStr)
    return True

def ReadDict(filepath):
    if filepath[0] == '~':
        filepath = os.path.expanduser(filepath)
    ext = os.path.splitext(filepath)[1]
    if ext=='.yaml':
        readDict = ReadDictYaml(filepath)
    elif ext=='.json':
        readDict = ReadDictJson(filepath)
    else:
        readDict = None
    return readDict

def WriteDict(outdict, filepath):
    if filepath[0] == '~':
        filepath = os.path.expanduser(filepath)
    ext = os.path.splitext(filepath)[1]
    if ext=='.yaml':
        readDict = WriteDictYaml(outdict, filepath)
    elif ext=='.json':
        readDict = WriteDictJson(outdict, filepath)
    else:
        readDict = None
    return readDict