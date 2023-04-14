import re

code_template = """#include <bits/stdc++.h>

{{code}}

int main(){{{{
{init}
{output}
    return 0;
}}}}
"""

func_template = """{return_type} {name}({parameter})
{{
    //Type Your Code Here
}}
"""

judge_template = """if(judge({parameter})!=0)
{{{{
    exit(114);
}}}}
"""

if_template = """\tif({para} {relation} {value}){{
\t\treturn -1;
\t}}
"""
str_template = """\tif(strcmp({para},{value}) {relation} 0){{
\t\treturn -1;
\t}}
"""

placeholder = {
    "int": "d",
    "short": "hd",
    "long": "ld",
    "long long": "lld",
    
    "unsigned short":"us",
    "unsigned int": "un",
    "unsigned long": "ul",
    "unsigned long long": "ull",
    
    "float": "f",
    "double": "lf",
    "long double": "Lf",
    "char": "c",
    "char*": "s"
}

relationship = {
    "=": "!=",
    "!=": "==",
    ">": "<=",
    ">=": "<",
    "<": ">=",
    "<=": ">"
}

judge_template_create = """int judge({para})
{{
{iiff}
\treturn 0;
}}
"""

data_type = ['int', 'short', 'long', 'float', 'double', 'char', 'int*', 'short*', 'long*', 'float*', 'double*', 'char*']

def CreateFunctionTemplate(name, return_type, parameter_list=None):
    
    if parameter_list:
        parameter = None
        parameter_list.sort(key=lambda x: x["id"])
        for para in parameter_list:
            if para["ptr"]:
                para_type = para["type"] + "*"
            else:
                para_type = para["type"]
            if parameter == None:
                parameter = "{} {}".format(para_type, para["name"])
            else:
                parameter += ", {} {}".format(para_type, para["name"])
            if para["arr"]:
                parameter += "[]"
        return func_template.format(return_type=return_type, name=name, parameter=parameter)
    else:
        return func_template.format(return_type=return_type, name=name, parameter="")


def CreateCodeTemplate(init, name, return_type, parameter_list):
    init = init.replace('{', '{{')
    init = init.replace('}', '}}')
    func = name
    if parameter_list:
        parameter_list.sort(key=lambda x: x["id"])
        for para in parameter_list:
            if func == name:
                func += "(" + para["name"]
            else:
                func += ", " + para["name"]
    func += ")"
    if return_type != "void":
        if return_type[-1] == "*":
            return_type = return_type[:-1]
            output = "printf(\"%{place_holder}\\n\",*({func}));\n".format(place_holder=placeholder[return_type], func=func)
        else:
            output = "printf(\"%{place_holder}\\n\",{func});\n".format(place_holder=placeholder[return_type], func=func)
    else:
        output = func + ";\n"
    return code_template.format(init=init, output=output)

def ResolveJudge(judge_code):
    ret = []
    if judge_code.split()[0] not in ['int','bool']:
        return False
    pos = 0 
    for pos in range(len(judge_code)):
        if judge_code[pos] == '(':
            judge_code = judge_code[pos+1:]
            break
    pos = 0 
    for pos in range(len(judge_code)):
        if judge_code[pos] == ')':
            judge_code = judge_code[:pos]
            break
    words = re.split("[, ]",judge_code)
    for str in words:
        if str not in data_type and str != '':
            if str[-2:] == "[]":
                ret.append(str[:-2])
            else:
                ret.append(str)
    return ret


def MergeSegment(code, judge_code):
    if code.find("$JUDGE$") == -1 or code.find("$CODE$") == -1:
        return False
    
    code = "#include <bits/stdc++.h>\n" + judge_code + code
    code = code.replace("{", "{{")
    code = code.replace("}", "}}")
    
    parameter = ""
    parameter_list = ResolveJudge(judge_code)
    for cond in parameter_list:
        if parameter == "":
            parameter = cond
        else:
            parameter += ", " + cond
    
    code = code.replace("$JUDGE$", judge_template.format(parameter=parameter) , 1)
    code = code.replace("$CODE$", "{code}", 1)
    return code

def CreateJudgeCode(condition):
    if_code = ""
    parameter_list = []
    used = {}
    for cond in condition:
        if not used.get(cond["parameter"]):
            if cond["data_type"] == "char[]":
                parameter_list.append(cond["data_type"][:-2] + " " + cond["parameter"] + "[]")
            else:
                parameter_list.append(cond["data_type"] + " " + cond["parameter"])
            used[cond["parameter"]] = True
        if cond["value_type"] != "const" and not used.get(cond["value"]):
            parameter_list.append(cond["value_type"] + " " + cond["value"])
            used[cond["value"]] = True
        if cond["data_type"] == "char[]":
            if cond["value_type"] != "const":
                if_code += str_template.format(para=cond["parameter"], relation=relationship[cond["relation"]], value=cond["value"])
            else:
                if_code += str_template.format(para=cond["parameter"], relation=relationship[cond["relation"]], value="\"" + cond["value"]+ "\"")
        else:    
            if_code += if_template.format(para=cond["parameter"], relation=relationship[cond["relation"]], value=cond["value"])
    return judge_template_create.format(para=', '.join(parameter_list), iiff=if_code)

def GetPassSum(name, config):
    if name == "format":
        if config["comma_space"]:
            return 4
        else:
            return 3
    elif name == "function":
        if config["disableIO"]:
            return 4
        else:
            return 3
    elif name == "memory":
        if config["check_ptr_free"]:
            return 2
        else:
            return 1
    elif name == "style":
        if config["single_name"]:
            return 5
        else:
            return 4
    else:
        return 2
            

condi = [
    {
        "parameter": "a",
        "data_type": "int",
        "relation": "=",
        "value": "b",
        "value_type": "int"
    },
    {
        "parameter": "a",
        "data_type": "int",
        "relation": "=",
        "value": "114514",
        "value_type": "const"
    },
    {
        "parameter": "c",
        "data_type": "char[]",
        "relation": "=",
        "value": "asdasd",
        "value_type": "const"
    }
]

# print(CreateJudgeCode(condi))
    