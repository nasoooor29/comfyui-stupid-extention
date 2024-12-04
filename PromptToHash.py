import hashlib

class PromptToHash:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "prompt": ("STRING", {"forceInput": True}),
                "defaultPath": ("STRING", {"default": "random/Comfyui", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("hash",)

    FUNCTION = "test"

    CATEGORY = "MyCustomNodes"

    def test(
        self,
        prompt: str,
        defaultPath:str
    ):
        try:
            h:str = hashlib.sha256(prompt.encode('utf-8'))
            return (h.hexdigest(),)
        except Exception as e:
            print(e)
            return (defaultPath,)