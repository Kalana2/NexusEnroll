import requests
import json
import time
from typing import Optional

BASE_URL = "http://localhost:8000"


class UserServiceTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.created_user_id: Optional[str] = None
        self.auth_token: Optional[str] = None

    def test_health_check(self):
        """Test health endpoint"""
        print("🔍 Testing health check...")
        try:
            response = requests.get(f"{self.base_url}/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            print("✅ Health check passed")
            return True
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False

    def test_create_user(self):
        """Test user creation"""
        print("\n👤 Testing user creation...")
        user_data = {
            "username": "john_doe_test",
            "email": "john.test@nexusenroll.edu",
            "first_name": "John",
            "last_name": "Doe",
            "password": "securepass123",
            "role": "Student",
        }

        try:
            response = requests.post(f"{self.base_url}/api/v1/users/", json=user_data)
            print(f"Status: {response.status_code}")

            if response.status_code == 201:
                data = response.json()
                self.created_user_id = data["user"]["id"]
                print(f"✅ User created successfully!")
                print(f"   User ID: {self.created_user_id}")
                print(f"   Username: {data['user']['username']}")
                print(f"   State: {data['user']['state']}")
                return True
            else:
                print(f"❌ User creation failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ User creation error: {e}")
            return False

    def test_get_user(self):
        """Test getting user by ID"""
        if not self.created_user_id:
            print("⏭️ Skipping get user test - no user created")
            return False

        print(f"\n📋 Testing get user by ID: {self.created_user_id}")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/users/{self.created_user_id}"
            )
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ User retrieved successfully!")
                print(f"   Username: {data['user']['username']}")
                print(f"   Email: {data['user']['email']}")
                print(f"   Role: {data['user']['role']}")
                print(f"   State: {data['user']['state']}")
                return True
            else:
                print(f"❌ Get user failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ Get user error: {e}")
            return False

    def test_activate_user(self):
        """Test user activation"""
        if not self.created_user_id:
            print("⏭️ Skipping activate user test - no user created")
            return False

        print(f"\n🔓 Testing user activation...")
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/users/{self.created_user_id}/activate"
            )
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ User activated successfully!")
                print(f"   New state: {data['user']['state']}")
                return True
            else:
                print(f"❌ User activation failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ User activation error: {e}")
            return False

    def test_login(self):
        """Test user login"""
        print(f"\n🔐 Testing user login...")
        login_data = {"username": "john_doe_test", "password": "securepass123"}

        try:
            response = requests.post(
                f"{self.base_url}/api/v1/users/auth/login", json=login_data
            )
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("token")
                print(f"✅ Login successful!")
                token_preview = (
                    f"{self.auth_token[:20]}..." if self.auth_token else "None"
                )
                print(f"   Token: {token_preview}")
                print(f"   Expires: {data.get('expires_at')}")
                return True
            else:
                print(f"❌ Login failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def test_update_user(self):
        """Test user update"""
        if not self.created_user_id:
            print("⏭️ Skipping update user test - no user created")
            return False

        print(f"\n✏️ Testing user update...")
        update_data = {"first_name": "John Updated", "last_name": "Doe Updated"}

        try:
            response = requests.put(
                f"{self.base_url}/api/v1/users/{self.created_user_id}", json=update_data
            )
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ User updated successfully!")
                print(
                    f"   New name: {data['user']['first_name']} {data['user']['last_name']}"
                )
                return True
            else:
                print(f"❌ User update failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ User update error: {e}")
            return False

    def test_assign_role(self):
        """Test role assignment"""
        if not self.created_user_id:
            print("⏭️ Skipping assign role test - no user created")
            return False

        print(f"\n👨‍🏫 Testing role assignment...")
        role_data = {"role": "Faculty"}

        try:
            response = requests.put(
                f"{self.base_url}/api/v1/users/{self.created_user_id}/role",
                json=role_data,
            )
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Role assigned successfully!")
                print(f"   New role: {data['user']['role']}")
                return True
            else:
                print(f"❌ Role assignment failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ Role assignment error: {e}")
            return False

    def test_list_users(self):
        """Test listing users"""
        print(f"\n📋 Testing list users...")
        try:
            # Test without filters
            response = requests.get(f"{self.base_url}/api/v1/users/")
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Users listed successfully!")
                print(f"   Total users: {data['count']}")

                # Test with role filter
                response = requests.get(f"{self.base_url}/api/v1/users/?role=Faculty")
                if response.status_code == 200:
                    filtered_data = response.json()
                    print(f"   Faculty users: {filtered_data['count']}")

                return True
            else:
                print(f"❌ List users failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ List users error: {e}")
            return False

    def test_duplicate_username(self):
        """Test duplicate username handling"""
        print(f"\n🔄 Testing duplicate username handling...")
        user_data = {
            "username": "john_doe_test",  # Same username
            "email": "different@email.com",
            "first_name": "Different",
            "last_name": "User",
            "password": "password123",
            "role": "Student",
        }

        try:
            response = requests.post(f"{self.base_url}/api/v1/users/", json=user_data)
            print(f"Status: {response.status_code}")

            if response.status_code == 400:
                print("✅ Duplicate username properly rejected!")
                return True
            else:
                print(f"❌ Duplicate username not handled: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ Duplicate username test error: {e}")
            return False

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting User Service API Tests")
        print("=" * 50)

        tests = [
            self.test_health_check,
            self.test_create_user,
            self.test_get_user,
            self.test_activate_user,
            self.test_login,
            self.test_update_user,
            self.test_assign_role,
            self.test_list_users,
            self.test_duplicate_username,
        ]

        passed = 0
        total = len(tests)

        for test in tests:
            try:
                if test():
                    passed += 1
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")

        print("\n" + "=" * 50)
        print(f"🎯 Test Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️ Some tests failed. Check the output above.")

        return passed == total


if __name__ == "__main__":
    tester = UserServiceTester()
    tester.run_all_tests()
