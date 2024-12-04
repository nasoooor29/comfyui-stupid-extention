import comfy
import comfy.samplers
from PIL import Image
import numpy as np


avaliableSamplers = {
    "KSampler //Inspire": {
        "positions": {"seed": 0, "steps": 2, "cfg": 3, "sampler": 4, "scheduler": 5}
    }
}
avaliablePromptNodeTypes = {
    "ShowText|pysssss": lambda node: node.get("widgets_values", ["0"])[0][0],
    "String Literal": lambda node: node.get("widgets_values", ["0"])[0],
    "CLIPTextEncode": lambda node: node.get("widgets_values", ["0"])[0],
}

avaliableCheckpointNodeTypes = {
    "CheckpointLoaderSimple": lambda node: node.get("widgets_values", ["0"])[0],
}


def GetSampler(PropName: str, samplerDict: dict):
    val = avaliableSamplers.get(PropName, None)
    if val == None:
        return None

    return {
        "scheduler": samplerDict["widgets_values"][val["positions"]["scheduler"]],
        "seed": samplerDict["widgets_values"][val["positions"]["seed"]],
        "steps": samplerDict["widgets_values"][val["positions"]["steps"]],
        "sampler": samplerDict["widgets_values"][val["positions"]["sampler"]],
        "cfg": samplerDict["widgets_values"][val["positions"]["cfg"]],
    }


def GetDictFunc(PropName: str, funcDict: dict, nodeDict: dict) -> str:
    f = funcDict.get(PropName, None)
    if f == None:
        return None
    return f(nodeDict)


def GetLorasFromStack(loraDict: dict) -> str:
    widgets_values = loraDict.get("widgets_values", ["0", "0"])[2:]
    formatted_strings = []

    def split_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i : i + chunk_size]

    for group in split_list(widgets_values, 4):
        if group[0] != "None":
            formatted_strings.append(f"<lora:{group[0]}:{group[1]}:{group[1]}>")

    result = " ".join(formatted_strings)
    return result


class DataGetter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "image": ("IMAGE", {"forceInput": True}),
                "sampler_node_name": ("STRING", {"multiline": False}),
                "positive_node_name": ("STRING", {"multiline": False}),
                "negative_node_name": ("STRING", {"multiline": False}),
                "LORA_STACK_node_name": ("STRING", {"multiline": False}),
                "checkpoint_node_name": ("STRING", {"multiline": False}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "INT",
        "INT",
        "INT",
        "INT",
        "FLOAT",
    )
    RETURN_NAMES = (
        "modelName",
        "scheduler",
        "positive prompt",
        "negative prompt",
        "seed",
        "width",
        "height",
        "steps",
        "cfg",
    )

    FUNCTION = "test"

    CATEGORY = "MyCustomNodes/LorasToPath"

    def test(
        self,
        image,
        sampler_node_name: str,
        positive_node_name: str,
        negative_node_name: str,
        LORA_STACK_node_name: str,
        checkpoint_node_name: str,
        prompt=None,
        extra_pnginfo=None,
    ):
        width = 0
        height = 0
        # with open(
        #     r"H:\h\ai\ai-test\ComfyUI\custom_nodes\MyCustomNodes\runme.py", "r"
        # ) as f:
        #     try:
        #         exec(f.read())
        #     except Exception as e:
        #         print(f"error: {e}")

        nodes = extra_pnginfo.get("workflow", {}).get("nodes", [])
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

        if len(image) >= 1:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            width = img.width
            height = img.height

        return (
            s.get("checkpoint", ""),
            s.get("scheduler", ""),
            s.get("positive prompt", ""),
            s.get("negative prompt", ""),
            s.get("seed", 0),
            width,
            height,
            s.get("steps", 0),
            s.get("cfg", 0),
        )
