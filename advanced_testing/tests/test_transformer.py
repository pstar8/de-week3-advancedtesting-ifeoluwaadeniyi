import pytest
from order_pipeline.transformer import Transformer

# Tests for parse_price()

def test_parse_price_with_currency_sign():
    transformer = Transformer()
    
    assert transformer.parse_price("$15.99") == 15.99
    assert transformer.parse_price("N500") == 500.0

def test_parse_price_string_number():
    transformer = Transformer()
    
    assert transformer.parse_price("100") == 100.0


def test_parse_price_with_text():
    transformer = Transformer()
    
    assert transformer.parse_price("45 dollars") == 45.0


def test_parse_price_float():
    transformer = Transformer()
    
    assert transformer.parse_price(15.99) == 15.99


def test_parse_price_with_whitespace():
    transformer = Transformer()
    
    assert transformer.parse_price("  $15.99  ") == 15.99


# Tests for quantity

def test_parse_quantity_from_integer():
    transformer = Transformer()
    
    assert transformer.parse_quantity(1) == 1


def test_parse_quantity_from_string():
    transformer = Transformer()
    
    assert transformer.parse_quantity("100") == 100


def test_parse_quantity_with_text():
    transformer = Transformer()

    assert transformer.parse_quantity("10units") == 10


def test_parse_quantity_with_whitespace():
    transformer = Transformer()
    
    assert transformer.parse_quantity("  3  ") == 3


# Tests for normalize_payment_status()

def test_normalize_payment_status_lowercase():
    transformer = Transformer()
    
    assert transformer.normalize_payment_status("paid") == "paid"
    assert transformer.normalize_payment_status("PAID") == "paid"
    assert transformer.normalize_payment_status("Refunded") == "refunded"
    assert transformer.normalize_payment_status("PaId") == "paid"


def test_normalize_payment_status_with_whitespace():
    transformer = Transformer()
    
    assert transformer.normalize_payment_status("  PAID  ") == "paid"
    assert transformer.normalize_payment_status(" pending ") == "pending"


# Tests for _clean_text_field()

def test_clean_text_field_whitespace():
    transformer = Transformer()
    
    assert transformer.clean_text_field("  Mouse") == "Mouse"
    assert transformer.clean_text_field("Keyboard   ") == "Keyboard"
    assert transformer.clean_text_field("  Wireless Mouse  ") == "Wireless Mouse"


def test_clean_text_field_empty_string():
    transformer = Transformer()
    
    assert transformer.clean_text_field("") == ""
    assert transformer.clean_text_field("   ") == ""


# Tests for _recalculate_total()

def test_recalculate_total_basic():
    transformer = Transformer()
    
    assert transformer.recalculate_total(2, 15.99) == 31.98
    assert transformer.recalculate_total(4, 12.75) == 51.0    
    assert transformer.recalculate_total(0, 15.99) == 0.0

# Tests for _transform_order()

def test_transform_order_basic():
    transformer = Transformer()
    
    input_order = {
        "order_id": "ORD001",
        "timestamp": "2025-10-19T08:00:00Z",
        "item": "  Wireless Mouse  ",
        "quantity": "2",
        "price": "$15.99",
        "payment_status": "PAID",
        "total": "$31.98"
    }
    
    result = transformer.transform_order(input_order)
    
    # Check transformations
    assert result["order_id"] == "ORD001"  # Cleaned
    assert result["item"] == "Wireless Mouse"  # Whitespace removed
    assert result["quantity"] == 2  # Converted to int
    assert result["price"] == 15.99  # Parsed to float
    assert result["payment_status"] == "paid"  # Normalized
    assert result["total"] == 31.98  # Recalculated