import pytest
from inventory import InMemoryInventory, InventoryError

@pytest.mark.bottomup
# Test flow : add -> reserve -> check -> relese -> check
def test_inventory_reserve_and_release():
    inv = InMemoryInventory()
    inv.add_stock("S", 5)
    inv.reserve("S", 3)
    assert inv.get_stock("S") == 2
    inv.release("S", 3)
    assert inv.get_stock("S") == 5

@pytest.mark.bottomup
# Test flow : when reserving more than available 
def test_inventory_not_enough_stock():
    inv = InMemoryInventory()
    inv.add_stock("S", 1)
    with pytest.raises(InventoryError):
        inv.reserve("S", 2)
        
@pytest.mark.bottomup
# Boundary Test: Reserve exact amount available (stock becomes 0)
def test_inventory_boundary_exact_amount():
    inv = InMemoryInventory()
    inv.add_stock("Z", 10)
    inv.reserve("Z", 10)
    assert inv.get_stock("Z") == 0
    # Ensure we can't reserve 1 more
    with pytest.raises(InventoryError):
        inv.reserve("Z", 1)

@pytest.mark.bottomup
# Boundary Test: Reserve 0 items (Should raise Error based on implementation)
def test_inventory_boundary_zero_qty():
    inv = InMemoryInventory()
    inv.add_stock("X", 5)
    
    with pytest.raises(InventoryError, match="qty must be > 0"):
        inv.reserve("X", 0)
        
    assert inv.get_stock("X") == 5