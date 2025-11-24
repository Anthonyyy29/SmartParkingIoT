"""
Smart Parking IoT - Example Client Scripts
Reference implementation untuk mengintegrasikan IoT device dengan FastAPI backend
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
ENTRY_ENDPOINT = f"{API_BASE_URL}/api/entry"
EXIT_ENDPOINT = f"{API_BASE_URL}/api/exit"
STATUS_ENDPOINT = f"{API_BASE_URL}/api/parking-status"
LAST_TRANSACTION_ENDPOINT = f"{API_BASE_URL}/api/last-transaction"


class SmartParkingClient:
    """Client untuk Smart Parking API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.entry_endpoint = f"{base_url}/api/entry"
        self.exit_endpoint = f"{base_url}/api/exit"
        self.status_endpoint = f"{base_url}/api/parking-status"
        self.last_transaction_endpoint = f"{base_url}/api/last-transaction"
    
    def record_entry(self, uid: str) -> Dict[str, Any]:
        """
        Record vehicle entry
        
        Args:
            uid (str): RFID UID of the vehicle
        
        Returns:
            dict: Response dari API
        """
        try:
            payload = {"uid": uid.strip()}
            response = requests.post(self.entry_endpoint, json=payload, timeout=5)
            data = response.json()
            
            if data.get("success"):
                print(f"✅ Vehicle entry recorded")
                print(f"   UID: {uid}")
                print(f"   Transaction ID: {data.get('transaction_id')}")
                print(f"   Entry Time: {data.get('entry_time')}")
            else:
                print(f"❌ Entry failed: {data.get('error')}")
            
            return data
        
        except requests.exceptions.ConnectionError:
            print("❌ Connection error: Cannot reach API server")
            return {"success": False, "error": "Connection refused"}
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"success": False, "error": str(e)}
    
    def record_exit(self, uid: str) -> Dict[str, Any]:
        """
        Record vehicle exit and get parking fee
        
        Args:
            uid (str): RFID UID of the vehicle
        
        Returns:
            dict: Response dari API dengan fee information
        """
        try:
            payload = {"uid": uid.strip()}
            response = requests.post(self.exit_endpoint, json=payload, timeout=5)
            data = response.json()
            
            if data.get("success"):
                print(f"✅ Vehicle exit recorded")
                print(f"   UID: {uid}")
                print(f"   Entry Time: {data.get('entry_time')}")
                print(f"   Exit Time: {data.get('exit_time')}")
                print(f"   Duration: {data.get('duration_minutes')} minutes")
                print(f"   Fee: Rp {data.get('fee'):,.0f}")
            else:
                print(f"❌ Exit failed: {data.get('error')}")
            
            return data
        
        except requests.exceptions.ConnectionError:
            print("❌ Connection error: Cannot reach API server")
            return {"success": False, "error": "Connection refused"}
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_parking_status(self) -> Dict[str, Any]:
        """
        Get current parking status (all active vehicles)
        
        Returns:
            dict: Response dari API dengan list kendaraan yang parkir
        """
        try:
            response = requests.get(self.status_endpoint, timeout=5)
            data = response.json()
            
            if data.get("success"):
                print(f"✅ Active vehicles: {data.get('active_vehicles')}")
                for vehicle in data.get("vehicles", []):
                    print(f"   - {vehicle['uid']}: {vehicle['duration_minutes']} min, Rp {vehicle['fee']:,.0f}")
            else:
                print(f"❌ Failed to get status: {data.get('error')}")
            
            return data
        
        except requests.exceptions.ConnectionError:
            print("❌ Connection error: Cannot reach API server")
            return {"success": False, "error": "Connection refused"}
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_last_transaction(self, uid: str) -> Dict[str, Any]:
        """
        Get last transaction for a specific vehicle
        
        Args:
            uid (str): RFID UID of the vehicle
        
        Returns:
            dict: Response dari API dengan transaction details
        """
        try:
            response = requests.get(f"{self.last_transaction_endpoint}/{uid}", timeout=5)
            data = response.json()
            
            if data.get("success"):
                print(f"✅ Last transaction for {uid}:")
                print(f"   Status: {data.get('status')}")
                print(f"   Entry: {data.get('entry_time')}")
                print(f"   Exit: {data.get('exit_time')}")
                print(f"   Duration: {data.get('duration_minutes')} min")
                print(f"   Fee: Rp {data.get('fee'):,.0f}")
            else:
                print(f"❌ Not found: {data.get('error')}")
            
            return data
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"success": False, "error": str(e)}


# ============================================================================
# EXAMPLE USAGE UNTUK ENTRY GATE
# ============================================================================

def entry_gate_example():
    """
    Contoh implementasi untuk gerbang masuk (entry gate)
    """
    print("\n" + "="*60)
    print("🚗 ENTRY GATE EXAMPLE")
    print("="*60)
    
    client = SmartParkingClient()
    
    # Simulasi: Baca RFID (dalam aplikasi nyata, baca dari sensor RFID)
    uid = "RFID001"
    
    # Record entry
    result = client.record_entry(uid)
    
    # Check result
    if result.get("success"):
        print("\n✅ Gate opened - Vehicle can enter")
        # TODO: Buka gerbang dengan relay/servo motor
        # TODO: Tampilkan pesan di LCD/display
    else:
        error_code = result.get("code", "UNKNOWN")
        print(f"\n❌ Gate closed - Error: {error_code}")
        # TODO: Tampilkan error di LCD/display


# ============================================================================
# EXAMPLE USAGE UNTUK EXIT GATE
# ============================================================================

def exit_gate_example():
    """
    Contoh implementasi untuk gerbang keluar (exit gate)
    """
    print("\n" + "="*60)
    print("🚗 EXIT GATE EXAMPLE")
    print("="*60)
    
    client = SmartParkingClient()
    
    # Simulasi: Baca RFID (dalam aplikasi nyata, baca dari sensor RFID)
    uid = "RFID001"
    
    # Record exit
    result = client.record_exit(uid)
    
    # Check result
    if result.get("success"):
        fee = result.get("fee")
        duration = result.get("duration_minutes")
        
        print(f"\n✅ Parking fee calculated")
        print(f"📊 Summary:")
        print(f"   Duration: {duration} minutes")
        print(f"   Fee: Rp {fee:,.0f}")
        
        # TODO: Tampilkan biaya di LCD/display
        # TODO: Buka gerbang
        # TODO: Optional: Print receipt
    else:
        error_code = result.get("code", "UNKNOWN")
        print(f"\n❌ Cannot process exit - Error: {error_code}")
        # TODO: Tampilkan error di LCD/display


# ============================================================================
# EXAMPLE USAGE UNTUK MONITORING (Admin Dashboard)
# ============================================================================

def admin_monitoring_example():
    """
    Contoh implementasi untuk monitoring (admin dashboard)
    """
    print("\n" + "="*60)
    print("📊 ADMIN MONITORING EXAMPLE")
    print("="*60)
    
    client = SmartParkingClient()
    
    # Get parking status
    status = client.get_parking_status()
    
    if status.get("success"):
        total_revenue = sum(v["fee"] for v in status.get("vehicles", []))
        print(f"\n💰 Total Revenue Today: Rp {total_revenue:,.0f}")


# ============================================================================
# EXAMPLE USAGE UNTUK QUERY SPECIFIC VEHICLE
# ============================================================================

def query_vehicle_example(uid: str):
    """
    Contoh query transaksi terakhir untuk vehicle tertentu
    """
    print("\n" + "="*60)
    print(f"🔍 QUERY VEHICLE: {uid}")
    print("="*60)
    
    client = SmartParkingClient()
    
    # Get last transaction
    transaction = client.get_last_transaction(uid)


# ============================================================================
# TESTING MAIN
# ============================================================================

if __name__ == "__main__":
    print("🅿️ Smart Parking IoT - Client Example")
    print("="*60)
    
    # Test connection
    print("\n1️⃣  Testing connection to API...")
    client = SmartParkingClient()
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Server is online!")
        else:
            print("❌ API Server returned error")
    except:
        print("❌ Cannot connect to API. Make sure FastAPI server is running!")
        print(f"   Run: python main.py")
        exit(1)
    
    # Run examples
    print("\n2️⃣  Running entry gate example...")
    entry_gate_example()
    
    print("\n3️⃣  Waiting 5 seconds before exit...")
    import time
    time.sleep(5)
    
    print("\n4️⃣  Running exit gate example...")
    exit_gate_example()
    
    print("\n5️⃣  Running admin monitoring example...")
    admin_monitoring_example()
    
    print("\n6️⃣  Querying specific vehicle...")
    query_vehicle_example("RFID001")
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)
