from .LorasToPath import LorasToPath
from .DataGetter import DataGetter
from .PromptToHash import PromptToHash


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "lora to path": LorasToPath,
    "DataGetter1032": DataGetter,
    "PromptToHash": PromptToHash,
}
 
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LorasToPath": "lora to path",
    "DataGetter1032": "Data Getter",
    "PromptToHash": "Prompt To Hash"
}

