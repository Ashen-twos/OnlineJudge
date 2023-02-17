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


parameter_list = [
    {
        "id": 5,
        "name": "a",
        "type": "int",
        "ptr": False,
        "arr": 0
    },
    {
        "id": 3,
        "name": "b",
        "type": "int",
        "ptr": False,
        "arr": 1024
    },
    {
        "id": 2,
        "name": "c",
        "type": "double",
        "ptr": True,
        "arr": 1024
    }
]

# print(CreateFunctionTemplate(name="sort", parameter_list=parameter_list, return_type="void"))
# print(CreateCodeTemplate(code="int add()", init="int a,b,c;", name="add", return_type="int*", parameter_list=parameter_list))

#temp = CreateCodeTemplate(init="int a,b,c;\nif(a>b){\na=b;\n}", name="add", return_type="int*", parameter_list=parameter_list)
#print(temp.format(code = "casdasdasda"))  