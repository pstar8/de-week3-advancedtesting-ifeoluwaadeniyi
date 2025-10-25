from typing import List, Dict


class Analyzer:
    
    def __init__(self):
        pass       
    
    def calculate_total_revenue(self, data: List[Dict]) -> float:
        total = 0.0
        
        for order in data:
            total += order['total']
        
        return total
    
    def calculate_average_revenue(self, data: List[Dict]) -> float:
        if len(data) == 0:
            return 0
        
        total_revenue = self.calculate_total_revenue(data)
        
        # Calculate average
        average = total_revenue / len(data)
        
        return average
    
    def count_payment_statuses(self, data: List[Dict]) -> Dict[str, int]:
        counts = {}
        
        for order in data:
            status = order['payment_status']
            
            if status not in counts:
                counts[status] = 0
            
            counts[status] += 1
        
        return counts

