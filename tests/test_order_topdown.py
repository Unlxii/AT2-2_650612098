import pytest
from inventory import InMemoryInventory
from shipping import ShippingService
from order import OrderService
from payment import PaymentDeclinedError
from emailer import EmailService

class StubFailPayment:
    def charge(self, amount: float, currency: str) -> str:
        raise PaymentDeclinedError("simulated decline")
    def refund(self, transaction_id: str) -> None:
        return
    
class StubSuccessPayment:
    def charge(self, amount, currency): return "tx_123"
    def refund(self, tid): pass
        
class StubConnectionErrorPayment:
    #(Connection Timeout)
    def charge(self, amount: float, currency: str) -> str:
        raise Exception("Connection Timeout")  # โยน Error ทั่วไป ไม่ใช่ PaymentDeclined
    def refund(self, transaction_id: str) -> None:
        pass
    
class SpyEmail(EmailService):
    def __init__(self):
        self.sent = []
    def send(self, to, subject, body):
        self.sent.append((to, subject, body))
        

@pytest.mark.topdown
# Payment fails -> Stock must be rolled back
def test_payment_decline_releases_stock():
    inv = InMemoryInventory()
    inv.add_stock("SKU1", 10)
    svc = OrderService(inv, StubFailPayment(), ShippingService(), SpyEmail())
    items = [{"sku":"SKU1","qty":3,"price":100.0,"weight":1.0}]
    with pytest.raises(PaymentDeclinedError):
        svc.place_order("a@b.com", items, region="TH")
    assert inv.get_stock("SKU1") == 10

@pytest.mark.topdown
# Order Success -> Verify Email Subject and Body
def test_order_success_check_email_content():
    inv = InMemoryInventory()
    inv.add_stock("SKU_A", 5)
    email_spy = SpyEmail()
    svc = OrderService(inv, StubSuccessPayment(), ShippingService(), email_spy)
    
    items = [{"sku":"SKU_A", "qty":1, "price":500, "weight":0.5}]
    svc.place_order("user@test.com", items, region="TH")
    # Assert Email Content
    assert len(email_spy.sent) == 1
    to, subject, body = email_spy.sent[0]
    assert to == "user@test.com"
    assert "Order confirmed" in subject  
    assert "SKU_A" in body               
    
@pytest.mark.topdown
# System/Network crash during payment
def test_system_error_handling():
    inv = InMemoryInventory()
    inv.add_stock("SKU_B", 5)
    svc = OrderService(inv, StubConnectionErrorPayment(), ShippingService(), SpyEmail())
    items = [{"sku":"SKU_B", "qty":1, "price":100, "weight":1}]

    with pytest.raises(Exception, match="Connection Timeout"):
        svc.place_order("fail@net.com", items, region="TH")
        
    assert inv.get_stock("SKU_B") == 4