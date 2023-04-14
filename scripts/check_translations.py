# _\(["'](.+[^\\])["']\)

import os
import re
import json


os.chdir(os.path.dirname(__file__) + "/..") # move to root project
os.chdir("elevenclock")


# Function to remove special characters from a string
def remove_special_chars(string):
    # Regular expression for special characters (excluding letters and digits)
    special_chars = r'[^a-zA-Z0-9]'
    # Use regular expression to remove special characters from the string
    return re.sub(special_chars, '', string)


# regex = r'_\(["\'](.+[^\\])["\']\)'
regex = r'(?<=_\(["\']).+?(?=["\']\))'
translation_strings: list[str] = []

for (dirpath, dirnames, filenames) in os.walk(".", topdown=True):
    for file in filenames:
        file_name, file_ext = os.path.splitext(file)
        if (file_ext != ".py"):
            continue
        f = open(os.path.join(dirpath, file), "r", encoding="utf-8")
        matches: list[str] = re.findall(regex, f.read())
        for match in matches:
            translation_strings.append(match.encode('raw_unicode_escape').decode('unicode_escape'))
        f.close()


translation_strings = list(set(translation_strings))
translation_strings.sort(key=lambda x: (remove_special_chars(x.lower()), x))
translation_obj: dict[str, str] = {}

for key in translation_strings:
    translation_obj[key] = None

# f = open("../my_dict.json", "w+", encoding="utf-8")
# json.dump(translation_obj, f, sort_keys=False, ensure_ascii=False, indent="  ")
# f.close()

# compare
f = open("lang/lang_en.json", "r", encoding="utf-8")
not_used: list[str] = []
lang_strings: dict[str, str] = json.load(f)
f.close()

for key in lang_strings.keys():
    if (key in translation_obj):
        del translation_obj[key]
    else:
        not_used.append(key)

f = open("../lang_compare.json", "w", encoding="utf-8")
output: dict[str, str] = {
    "not_used": not_used,
    "not_translated": list(translation_obj),
}
json.dump(output, f, ensure_ascii=False, indent="  ")
f.close()        

output: list[str] = []

output.append('''
       dasd
       sdasd
       ''')

if (len(not_used) > 0):
    output.append("Not used:")
    output.append("```")
    output.append("\n".join(not_used))
    output.append("```")
    output.append("")

if (len(translation_obj.keys()) > 0):
    output.append("Not translated:")
    output.append("```")
    output.append("\n".join(translation_obj.keys()))
    output.append("```")
    output.append("")

f = open("../pull_request.md", "w+", encoding="utf-8")
f.write("\n".join(output))
f.close()
