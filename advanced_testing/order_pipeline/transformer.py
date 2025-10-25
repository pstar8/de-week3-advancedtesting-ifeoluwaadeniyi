from typing import List, Dict
import re  


class Transformer:
    
    def __init__(self):
        pass
    
    # def transform(self, data: List[Dict]) -> List[Dict]:
    #     transformed_data = []
    #     for order in data:
    #         transformed_order = self.transform_order(order)
    #         transformed_data.append(transformed_order)
    #     return transformed_data
    
    
    def parse_price(self, value) -> float:
        if isinstance(value, (int, float)):
            return float(value)

        value_str = str(value).strip().replace("$", "").replace(",", "")
         # return float(value_str)

        pattern = r'[\$N]?(\d+\.?\d*)'

        match = re.match(pattern, value_str) 

        if match:
            number_str = match.group(1)
            return float(number_str)

        raise ValueError(f"Could not parse price: {value}") 
  
    def parse_quantity(self, value) -> int:
        if value is None:
            raise ValueError("Quantity cannot be None")
        if isinstance(value, int):
            return value
        value_str = str(value).strip().replace("units", "").replace("pcs", "").replace("pieces", "")
        if value_str.isdigit():
            return int(value_str)
        raise ValueError(f"Could not parse quantity: {value}")
    
    def normalize_payment_status(self, status: str) -> str:
        normalized_status = status.strip().lower()
        return normalized_status
    
    def clean_text_field(self, text: str) -> str:
        return text.strip().title()
    
    def recalculate_total(self, quantity: int, price: float) -> float:
        return round(quantity * price, 2)
       
    def transform_order(self, order: Dict) -> Dict:
        transformed = {}
    
        transformed["order_id"] = (order["order_id"])
        transformed["timestamp"] = (order[("timestamp")])
        transformed["item"] = self.clean_text_field(order["item"])
        
        transformed["quantity"] = self.parse_quantity(order.get("quantity"))
        transformed["price"] = self.parse_price(order.get("price"))
        
        transformed["payment_status"] = self.normalize_payment_status(str(order.get("payment_status")))
        
       
        transformed["total"] = self.recalculate_total(
            transformed["quantity"], 
            transformed["price"]
        )
        return transformed
    