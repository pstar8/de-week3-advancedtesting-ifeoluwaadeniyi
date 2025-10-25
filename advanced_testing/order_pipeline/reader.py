import json
from typing import List, Dict

class Reader:

    #Reads JSON file

    def __init__ (self, filepath:str):
        self.filepath = filepath

    def read(self) -> List[Dict]:
        try:
          with open(self.filepath, 'r', encoding='utf-8') as file:
              data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format")
        
        if len(data) == 0:
            raise ValueError("The JSON file is empty")
        
        return data
