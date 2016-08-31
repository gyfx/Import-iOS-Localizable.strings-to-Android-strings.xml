import xml.dom.minidom
from collections import OrderedDict
from xml.etree.ElementTree import tostring, parse, Element
android_zh_file_path = "C:\\path\\app\\src\\main\\res\\values-zh-rCN\\strings.xml";
android_paths = ["C:\\path\\app\\src\\main\\res\\values-de\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-el\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-en-rUS\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-es\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-fr\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-it\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-ja\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-ko\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-pt\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-ru\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-th\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-tr\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-zh-rTW\\strings.xml",
                 "C:\\path\\app\\src\\main\\res\\values-vi\\strings.xml"]
ios_paths = ["iOS/de.lproj/Localizable.strings",
             "iOS/el.lproj/Localizable.strings",
             "iOS/en.lproj/Localizable.strings",
             "iOS/en_US.lproj/Localizable.strings",
             "iOS/es_ES.lproj/Localizable.strings",
             "iOS/fr.lproj/Localizable.strings",
             "iOS/it.lproj/Localizable.strings",
             "iOS/ja.lproj/Localizable.strings",
             "iOS/ko.lproj/Localizable.strings",
             "iOS/pt_PT.lproj/Localizable.strings",
             "iOS/ru.lproj/Localizable.strings",
             "iOS/th.lproj/Localizable.strings",
             "iOS/tr.lproj/Localizable.strings",
             "iOS/zh_Hant.lproj/Localizable.strings",
             "iOS/vi.lproj/Localizable.strings"
             ]
# 特殊情况
local_dict = {
    "local_refund_description": "退款说明\\n一、申请退款。。。",

}


def dict_to_xml(tag, d):
    elem = Element(tag)
    for string123 in d:
        child = Element("string")
        child.text = d[string123]
        child.set("name", string123)
        elem.append(child)
    return elem


def get_android_values_dict(path):
    dom_tree = xml.dom.minidom.parse(path)
    collection = dom_tree.documentElement
    strings = collection.getElementsByTagName("string")
    temp_dict = OrderedDict()
    for string in strings:
        key = string.getAttribute("name")
        value = string.childNodes[0].data
        temp_dict[key] = value
    return temp_dict


def get_ios_values_dict(path):
    file_object = open(path, 'r', encoding="UTF-8")
    strings1 = file_object.readlines()
    temp_dict_ios = OrderedDict()
    for string in strings1:
        if string != "\n":
            key_vaule = string.split("=")
            if len(key_vaule) != 2:
                print(key_vaule)
                raise IndexError(len(key_vaule))
            if not key_vaule[0].startswith("\"") or not key_vaule[0].endswith("\" ") or not key_vaule[1].startswith(
                    " \"") or not \
                    key_vaule[1].endswith("\";\n"):
                print(key_vaule)
                print(not key_vaule[0].startswith("\""))
                print(not key_vaule[0].endswith("\" "))
                print(not key_vaule[1].startswith(" \""))
                print(not key_vaule[1].endswith("\";\n"))
                raise Exception(len(key_vaule))
            key = key_vaule[0][1:-2]
            value = key_vaule[1][2:-3]
            value = value.replace("'", "\\'")
            if key in local_dict:
                key = local_dict[key]
            for j in range(key.count("%@")):
                temp_str = "%" + str(j + 1) + "$s"
                key = key.replace("%@", temp_str, 1)
            for k in range(value.count("%@")):
                temp_str1 = "%" + str(k + 1) + "$s"
                value = value.replace("%@", temp_str1, 1)
            temp_dict_ios[key] = value
    file_object.close()
    return temp_dict_ios


def find_android_ios_repeat(ios, android):
    repeat_dict = OrderedDict()
    for key in android:
        if android[key] in ios:
            repeat_dict[key] = android[key]
    return repeat_dict


def get_final_dict(ios_target_dict, repeat_dict, android_target_dict):
    for key in repeat_dict:
        android_target_dict[key] = ios_target_dict[repeat_dict[key]]
    return android_target_dict


def write_dict_to_file(dict1, path1):
    e = dict_to_xml('resources', dict1)
    file_object = open(path1, 'wb')
    file_object.write(tostring(e, 'utf-8'))
    file_object.close()


def get_final_xml(ios_target_dict, repeat_dict, android_xml_path):
    doc = parse(android_xml_path)
    temp_list = []
    root = doc.getroot()
    for item in root:
        temp_list.append(item.attrib.get('name'))
    for key in repeat_dict.keys():
        if key in temp_list:
            for item in root:
                if item.attrib.get('name') == key:
                    item.text = ios_target_dict[repeat_dict[key]]
                    break
        else:
            e = Element('string', {"name": key})
            e.text = ios_target_dict[repeat_dict[key]]
            root.append(e)

    return doc
    # for key in repeat_dict:
    #     android_target_dict[key] = ios_target_dict[repeat_dict[key]]
    # return android_target_dict


repeat = find_android_ios_repeat(get_ios_values_dict("iOS/en.lproj/Localizable.strings"), get_android_values_dict(
    android_zh_file_path))

for i in range(android_paths.__len__()):
    temp = get_final_xml(get_ios_values_dict(ios_paths[i]), repeat, android_paths[i])
    # print(temp.__len__())
    # write_dict_to_file(temp, android_paths[i])
    temp.write(android_paths[i], encoding="utf-8", xml_declaration=True)
    print(i)
