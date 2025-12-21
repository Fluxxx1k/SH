#!/usr/bin/env python3
"""
Test script to demonstrate error handling functionality
"""

import requests
import json

def test_error_pages():
    """Test different error pages"""
    base_url = "http://localhost:20050"
    
    print("Testing error pages...")
    
    # Test 404 error
    print("\n1. Testing 404 error:")
    try:
        response = requests.get(f"{base_url}/nonexistent-page")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("✓ 404 error page works correctly")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing 404: {e}")
    
    # Test manual error route
    print("\n2. Testing manual error route:")
    try:
        response = requests.get(f"{base_url}/error?code=500&message=Test+Error&description=This+is+a+test+error&comment=Test+comment")
        print(f"Status: {response.status_code}")
        if response.status_code == 500:
            print("✓ Manual error route works correctly")
            # Check if error page contains expected elements
            if "Test Error" in response.text:
                print("✓ Error message displayed correctly")
            if "This is a test error" in response.text:
                print("✓ Error description displayed correctly")
            if "Test comment" in response.text:
                print("✓ Error comment displayed correctly")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing manual error route: {e}")
    
    # Test different error codes
    error_codes = [400, 401, 403, 404, 405, 500]
    for code in error_codes:
        print(f"\n3. Testing error code {code}:")
        try:
            response = requests.get(f"{base_url}/error?code={code}")
            print(f"Status: {response.status_code}")
            if response.status_code == code:
                print(f"✓ Error code {code} works correctly")
            else:
                print(f"✗ Unexpected status code: {response.status_code}")
        except Exception as e:
            print(f"✗ Error testing code {code}: {e}")

def test_protected_routes():
    """Test routes that should trigger errors when not logged in"""
    base_url = "http://localhost:20050"
    
    print("\n\nTesting protected routes (should trigger 401 or redirect)...")
    
    # Test lobby without login
    print("\n1. Testing lobby without login:")
    try:
        response = requests.get(f"{base_url}/lobby", allow_redirects=False)
        print(f"Status: {response.status_code}")
        if response.status_code in [301, 302, 401]:
            print("✓ Protected route correctly redirects/requires auth")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing lobby: {e}")

def main():
    """Main test function"""
    print("=" * 60)
    print("Secret Hitler Error Handling Test Suite")
    print("=" * 60)
    
    # Check if server is running
    base_url = "http://localhost:20050"
    try:
        response = requests.get(base_url, timeout=5)
        print("✓ Server is running")
        
        test_error_pages()
        test_protected_routes()
        
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running. Please start the server first:")
        print("  python app.py")
        print("\nThen run this test script again.")
    except Exception as e:
        print(f"✗ Error connecting to server: {e}")
    
    print("\n" + "=" * 60)
    print("Test suite completed")
    print("=" * 60)

if __name__ == "__main__":
    main()