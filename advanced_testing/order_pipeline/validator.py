from typing import Dict
from typing import List


class Validator:
    def has_required_fields(self, order: Dict) -> bool:
        required_fields = {"order_id", "timestamp", "item", "quantity", "price", "total", "payment_status"}
        
        for field in required_fields:
            if field not in order:
                return False    
        return True
    
    def numeric_fields_are_present_and_positive(self, order: Dict) -> bool:

        numeric_fields = ["quantity", "price", "total"]
        for field in numeric_fields:
            value = order.get(field)
            if value is None:
                return False
            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                return False
            if numeric_value <= 0:
                return False
        return True
        

    def validate(self, data: List[Dict]) -> List[Dict]:
        valid_orders = []
        self.invalid_orders = []
        
        for order in data:
            if self.is_valid_order(order):
                valid_orders.append(order)  # Include good orders
            else:
                self.invalid_orders.append(order)  # Skip bad orders
        
        return valid_orders

    def is_valid_order(self, order: Dict) -> bool:
        # All conditions must be True
            return (
                self.has_required_fields(order) and 
                self.numeric_fields_are_present_and_positive(order)
                # self.validate(order)
            )