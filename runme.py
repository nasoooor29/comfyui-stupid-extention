print("======================================[START]======================================")

from .DataGetter import *


nodes = (
    current_extra_data
    .get("workflow", {})
    .get("nodes", [])
)
print(nodes)
comfy.samplers.KSampler.SAMPLERS
s = {}
for node in nodes:
    node_title = node.get("title", None)
    if not node_title:
        continue
    PropName = node.get("properties", {}).get("Node name for S&R", "")
    if sampler_node_name == node_title:
        samplerData = GetSampler(PropName, node)
        if s == None:
            print("sampler data could not be found")
            continue
        s.update(samplerData)
    elif positive_node_name == node_title or negative_node_name == node_title:
        pType = "positive" if positive_node_name == node_title else "negative"
        p = GetDictFunc(PropName, avaliablePromptNodeTypes, node)
        if not p:
            print(f"{pType} prompt could not be found")
            continue
        s[f"{pType} prompt"] = p
    elif checkpoint_node_name == node_title:
        ckpt = GetDictFunc(PropName, avaliableCheckpointNodeTypes, node)
        if not ckpt:
            print("checkpoint could not be found")
            continue
        s["checkpoint"] = ckpt
    elif LORA_STACK_node_name == node_title:
        stackStr = GetLorasFromStack(node)
        p = s.get("positive prompt", "")
        s["positive prompt"] = f"{stackStr}\n\n{p}"


for k, v in s.items():
    print(f"{k}: {v}")


print("======================================[END]======================================")