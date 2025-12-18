from inventory import InMemoryInventory
from payment import SimplePayment
from shipping import ShippingService
from order import OrderService
from emailer import EmailService
import pytest

class SpyEmail(EmailService):
    def __init__(self): self.calls = 0
    def send(self, to, subject, body): self.calls += 1
    
@pytest.mark.sandwich
def test_order_success_with_real_payment():
    inv = InMemoryInventory()
    inv.add_stock("A", 2)
    svc = OrderService(inv, SimplePayment(), ShippingService(), SpyEmail())
    items = [{"sku":"A","qty":1,"price":900.0,"weight":2.0}]
    res = svc.place_order("x@y.com", items, region="TH")
    assert inv.get_stock("A") == 1

@pytest.mark.sandwich
# Sandwich: Test logic with different Region (US)
def test_order_us_region_integration():
    inv = InMemoryInventory()
    inv.add_stock("IPHONE", 10)
    email_spy = SpyEmail()
    svc = OrderService(inv, SimplePayment(), ShippingService(), email_spy)
    
    # Large items shipped to the US (shipping costs will likely be higher based on the logic of actual shipping services).
    items = [{"sku":"IPHONE", "qty":2, "price":200.0, "weight":0.5}]
    
    res = svc.place_order("usa_user@example.com", items, region="US")
    # check Integration
    assert inv.get_stock("IPHONE") == 8
    assert email_spy.calls == 1
    assert res['total'] > (200.0 * 2)