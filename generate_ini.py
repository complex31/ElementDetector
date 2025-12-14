import os
import sys
import subprocess as sp
import json
from enum import Enum

class Element(Enum):
    anemo = 0
    geo = 1
    electro = 2
    dendro = 3
    hydro = 4
    pyro = 5
    cryo = 6
    other = 7

traveler_skill = {
    Element.anemo: "a60e8d48",
    Element.geo: "43539c54",
    Element.electro: "e0347092",
    Element.dendro: "0668174a",
    Element.hydro: "7a16f342",
    Element.pyro: "3cae7041",
    Element.cryo: "00000000",
}

assets_path = "../../../GI-Model-Importer-Assets/PlayerCharacterData"

def getCharacterElement(name, ref):
    for element in ref:
        if name in ref[element]:
            return Element[element]
    print(f"using other element for {name}")
    return Element.other
    
def getHashFromJson(name):
    hashFile = open(f"{assets_path}/{name}/hash.json")
    hashData = json.load(hashFile)
    hashFile.close()
    #print(hashData);
    for component in hashData:
        if(len(component['component_name']) == 0):
            return component['position_vb']
    for component in hashData:
        if(component['component_name'] == "Body"):
            return component['position_vb']
    print(f"hash not found {name}")
    return 'notfound'
    
def getIniSection(name, hash, element):
    lines = [
        f"[TextureOverride{name}]",
        f"hash = {hash}",
        "match_priority = 0",
        f"run = CommandListActive{element.name.capitalize()}"
    ]
    return lines
    
names = os.listdir(assets_path)
names.sort()

refFile = open("reference.json")
refData = json.load(refFile)
#print(refdata)

output = open("detector.ini", "w")

leadingLines = [
    "namespace = global\\detector",
    "",
    "[Constants]",
    f"global $element = {Element.other.value}",
    f"global persist $travelerElement = {Element.other.value}",
    "",
    ";" + "#"*30,
    ""
]

chunk = '\n'.join(leadingLines) + '\n'
output.write(chunk)

# generate overrides
for name in names:
    if "Mod" in name:
        continue
    overrideLines = getIniSection(name, getHashFromJson(name), getCharacterElement(name, refData))
    chunk = '\n'.join(overrideLines) + '\n;'+'-'*30 + '\n'
    output.write(chunk)

for element in traveler_skill:
    overrideLines = [
        f"[TextureOverrideTraveler{element.name.capitalize()}]",
        f"hash = {traveler_skill[element]}",
        f"$travelerElement = {element.value}"
    ]
    chunk = '\n'.join(overrideLines) + '\n;'+'-'*30 + '\n'
    output.write(chunk)

for name in refData["other"]:
    overrideLines = [
        f"[TextureOverride{name}]",
        f"hash = {hash}",
        f"run = CommandListActiveTravelerElement"
    ]

output.write("\n\n")
# generate commandlist
for element in Element:
    if element == Element.other:
        continue
    commandLines = [
        f"[CommandListActive{element.name.capitalize()}]",
        f"$element = {element.value}"
    ]
    chunk = '\n'.join(commandLines) + '\n'
    output.write(chunk)

commandLines = [
    f"[CommandListActiveOther]",
    f"$element = $travelerElement"
]
chunk = '\n'.join(commandLines) + '\n'
output.write(chunk)

refFile.close()
output.close()