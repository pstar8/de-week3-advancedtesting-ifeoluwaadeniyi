from typing import Dict
from typing import List


class Validator:

    def __init__(self):
        self.invalid_orders = []

    def has_required_fields(self, order: Dict) -> bool:
        required_fields = {"order_id", "timestamp", "item", "quantity", "price", "total", "payment_status"}
        
        for field in required_fields:
            if field not in order:
                return False    
        return True
    
    def fields_are_not_empty(self, order: Dict) -> bool:
        required_fields = {"order_id", "timestamp", "item", "quantity", "price", "total", "payment_status"}
        for field in required_fields:
            value = order.get(field)
            
            if value is None:
                return False
            
            # If string, check if empty or just whitespace
            if isinstance(value, str):
                if value.strip() == "":
                    return False
        
        return True


    def numeric_fields_are_positive(self, order: Dict) -> bool:
        numeric_fields = ['quantity', 'price', 'total']
        
        for field in numeric_fields:
            value = order.get(field)
            
            # Only check if it's already a number
            if isinstance(value, (int, float)):
                if value <= 0:
                    return False
        
        return True

    def numeric_fields_are_parseable(self, order: Dict) -> bool:
        """Check if numeric fields can be converted to numbers."""
        
        INVALID_VALUES = ['n/a', 'na', 'unknown', 'none', 'null', '']
        
        numeric_fields = ['quantity', 'price', 'total']
        
        for field in numeric_fields:
            value = order.get(field)
            
            if isinstance(value, (int, float)):
                continue
            
            # If it's a string, check if it's in the list
            if isinstance(value, str):
                value_lower = value.strip().lower()
                if value_lower in INVALID_VALUES:
                    return False
        
        return True
    def validate(self, data: List[Dict]) -> List[Dict]:
        valid_orders = []
        self.invalid_orders = []
        
        for order in data:
            if self.is_valid_order(order):
                valid_orders.append(order)
            else:
                self.invalid_orders.append(order)
        
        return valid_orders

    def is_valid_order(self, order: Dict) -> bool:
        return (
            self.has_required_fields(order) and 
            self.fields_are_not_empty(order) and
            self.numeric_fields_are_positive(order) and
            self.numeric_fields_are_parseable(order)
        )