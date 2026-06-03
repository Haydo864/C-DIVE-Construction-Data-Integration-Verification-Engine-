from fastapi.testclient import TestClient
from main import app

# This creates a fake browser that talks directly to your FastAPI code
client = TestClient(app)

def test_successful_extraction():
    """Test that a perfect invoice returns a Green status."""
    fake_invoice = "Invoice from ProBuild. Date: 2024-01-10. Total: $1000. Line 1: Lumber $600. Line 2: Nails $400."
    
    response = client.post("/api/process-invoice", json={"raw_text": fake_invoice})
    
    # 1. Did the server respond without crashing?
    assert response.status_code == 200
    
    data = response.json()
    
    # 2. Did it pass the math check?
    assert data["status"] == "Green"
    assert len(data["flags"]) == 0
    
    # 3. Did the AI extract the vendor name correctly?
    assert data["data"]["vendor_name"] == "ProBuild"


def test_math_fail_safe():
    """Test that a mathematically incorrect invoice is caught and flagged Red."""
    # Notice the total says $5000, but the line items only add up to $1000!
    bad_invoice = "Invoice from ProBuild. Date: 2024-01-10. Total: $5000. Line 1: Lumber $600. Line 2: Nails $400."
    
    response = client.post("/api/process-invoice", json={"raw_text": bad_invoice})
    assert response.status_code == 200
    
    data = response.json()
    
    # 1. Did our deterministic Python code catch the error?
    assert data["status"] == "Red"
    
    # 2. Did it generate the specific warning flag?
    assert len(data["flags"]) == 1
    assert "Math Error" in data["flags"][0]