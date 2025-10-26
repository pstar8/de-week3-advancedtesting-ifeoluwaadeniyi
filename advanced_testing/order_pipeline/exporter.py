import json
from typing import List, Dict


class Exporter:
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def export(self, data: List[Dict]) -> None:
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            print(f"✅ Successfully exported {len(data)} orders to {self.filepath}")

        except IOError as e:
            raise IOError(f"Failed to write to file: {self.filepath}. Error: {str(e)}")
        
        except Exception as e:
            raise ValueError(f"Failed to serialize data to JSON: {str(e)}")