

class LorasToPath:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "loras": ("STRING", {"forceInput": True}),
                "keyword_on_lora": ("STRING", {"default": "chara", "multiline": False}),
                "default_value": ("STRING", {"default": "random/Comfyui", "multiline": False}),
            },
        }
 
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("path", )
 
    FUNCTION = "test"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "MyCustomNodes/LorasToPath"
 
    def test(self, loras, keyword_on_lora:str, default_value:str):
        print(loras)
        print(keyword_on_lora)
        print(default_value)
        try:
            for lora in loras.split(">"):
                loraArr = lora.split(">")[0].split(":")
                if len(loraArr) > 2:
                    print("fuck3")
                    loraName = loraArr[1].rsplit(".", 1)[0]
                    if keyword_on_lora.lower() in loraName.lower():
                        return (loraName, )
        except Exception as e:
            print(e)
            return (default_value, )

        return (default_value, )
 
