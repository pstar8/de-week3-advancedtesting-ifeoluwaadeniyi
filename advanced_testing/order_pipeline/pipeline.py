import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List
from typing import Dict
from order_pipeline.reader import Reader
from order_pipeline.validator import Validator
from order_pipeline.transformer import Transformer
from order_pipeline.analyzer import Analyzer
from order_pipeline.exporter import Exporter


class Pipeline:    
    def __init__(self, input_file: str, output_file: str):
       
        self.input_file = input_file
        self.output_file = output_file
    
    def run(self) -> Dict:
        """Read the data"""
        print(f"📖 Reading data from {self.input_file}...")
        reader = Reader(self.input_file)
        raw_data = reader.read()
        print(f"   ✅ Read {len(raw_data)} orders")
        
        """Validate the data"""
        print(f"\n🔍 Validating data...")
        validator = Validator()
        valid_data = validator.validate(raw_data)
        print(f"   ✅ {len(valid_data)} valid orders")
        print(f"   ⚠️  {len(validator.invalid_orders)} invalid orders skipped")
        
        """Transform the data"""
        print(f"\n🔄 Transforming data...")
        transformer = Transformer()
        clean_data = transformer.transform(valid_data)
        print(f"   ✅ Transformed {len(clean_data)} orders")
        
        """Validate the data"""
        print(f"\n📊 Analyzing data...")
        analyzer = Analyzer()
        analytics = analyzer.analyze(clean_data)
        print(f"   ✅ Total Revenue: ${analytics['total_revenue']:.2f}")
        print(f"   ✅ Average Revenue: ${analytics['average_revenue']:.2f}")
        print(f"   ✅ Payment Status Breakdown:")
        for status, count in analytics['payment_status_counts'].items():
            print(f"      - {status}: {count}")
        
        """Export the data"""
        print(f"\n💾 Exporting cleaned data to {self.output_file}...")
        exporter = Exporter(self.output_file)
        exporter.export(clean_data)
        print(f"   ✅ Exported {len(clean_data)} orders")
        
        print(f"\n🎉 Pipeline completed successfully!")
        return analytics


if __name__ == '__main__':
    pipeline = Pipeline('shoplink.json', 'shoplink_cleaned.json')
    results = pipeline.run()
    