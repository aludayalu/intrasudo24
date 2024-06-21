import uuid, json

def render(path, variables=None):
    component=open(path).read()
    if variables==None:
        variables=locals()|globals()
    replace_maps={}
    for variable in variables:
        if "{"+variable+"}" in component:
            uid=uuid.uuid4().__str__()
            replace_maps[uid]=variable
            component=component.replace("{"+variable+"}", uid)
    for x in replace_maps:
        out=variables[replace_maps[x]]
        if type(out) in [int, float, dict]:
            out=json.dumps(out)
        if type(out)==list:
            out="\n".join([str(x) for x in out])
        component=component.replace(x, out)
    return component