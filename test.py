import requests
import unittest

class TestProjectServer(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000"
        self.valid_user = {"username": "0123", "password": "0123-pw"}
        self.pi_url = f"{self.base_url}/pi"
        self.quote_url = f"{self.base_url}/quote"
    # R1 (3)/3 401
    def test_missing_user_info(self):
        # Omitting user information to test 401 response
        response = requests.post(self.pi_url, json={})
        self.assertEqual(response.status_code, 401)
        self.assertIn("user info error", response.json()['error'])
    
    def test_invalid_username(self):
        # Using invalid username to test 401 response
        response = requests.post(self.pi_url, json={"username": "a123", "password": "a123-pw"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("user info error", response.json()['error'])

    def test_invalid_password(self):
        # Using invalid password to test 401 response
        response = requests.post(self.pi_url, json={"username": "0123", "password": "0123-pw-wrong"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("user info error", response.json()['error'])

    # R3 pi web service (9)/7
    #400 3/2
    #200 6/5
    def test_missing_simulations(self):
        # Missing simulations field in request
        response = requests.post(self.pi_url, json={**self.valid_user})
        self.assertEqual(response.status_code, 400)
        #self.assertIn("error", response.json())
        self.assertIn("missing field simulations", response.json()['error'])

    def test_invalid_simulations(self):
        # Invalid simulations field in request
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 99})
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field simulations", response.json()['error'])

    def test_valid_simulations_lower_bound(self):
        # Valid simulations field in request(lower bound)
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100})
        self.assertEqual(response.status_code, 200)
        self.assertIn("calculated_value_of_pi", response.json())

    def test_valid_simulations_upper_bound(self):
        # Valid simulations field in request(uppper bound)
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100000000})
        self.assertEqual(response.status_code, 200)
        self.assertIn("calculated_value_of_pi", response.json())

    def test_missing_concurrency(self):
        # Missing concurrency field in request
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100})
        self.assertEqual(response.status_code, 200)
        self.assertIn("calculated_value_of_pi", response.json())
    
    def test_invalid_concurrency(self):
        # Invalid concurrency field in request
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100, "concurrency": 9})
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field concurrency", response.json()['error'])
    
    def test_valid_concurrency_lower_bound(self):
        # Valid concurrency field in request(lower bound)
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100, "concurrency": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("calculated_value_of_pi", response.json())
    
    def test_valid_concurrency_upper_bound(self):
        # Valid concurrency field in request(upper bound)
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100, "concurrency": 8})
        self.assertEqual(response.status_code, 200)
        self.assertIn("calculated_value_of_pi", response.json())
    
    def test_valid_concurrency_default(self):
        # Valid concurrency field in request(default)
        response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100})
        self.assertEqual(response.status_code, 200)
        self.assertIn("calculated_value_of_pi", response.json())
    # ------------------------end of R2

    # def test_pi_service_approximate_value(self):
    #     # Valid request to pi service should return approximate value of pi
    #     response = requests.post(self.pi_url, json={**self.valid_user, "simulations": 100})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("pi", response.json())

    # R4 quote web service (8)/8
    def test_missing_protocol(self):
        # Missing protocol field in request
        response = requests.post(self.quote_url, json={**self.valid_user})
        self.assertEqual(response.status_code, 400)
        self.assertIn("missing field protocol", response.json()['error'])

    def test_invalid_protocol(self):
        # Invalid protocol field in request
        response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "invalid"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field protocol", response.json()['error'])

    def test_valid_protocol(self):
        # Valid protocol field in request
        response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "tcp"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("quotes", response.json())

    def test_valid_protocol_udp(self):
        # Valid protocol field in request
        response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "udp"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("quotes", response.json())

    def test_invalid_concurrency(self):
        # Invalid concurrency field in request
        response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "tcp", "concurrency": 9})
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field concurrency", response.json()['error'])
    
    def test_valid_concurrency_lower_bound(self):
        # Valid concurrency field in request(lower bound)
        response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "tcp", "concurrency": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("quotes", response.json())
    
    def test_valid_concurrency_upper_bound(self):
        # Valid concurrency field in request(upper bound)
        response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "tcp", "concurrency": 8})
        self.assertEqual(response.status_code, 200)
        self.assertIn("quotes", response.json())
    
    def test_valid_concurrency_default(self):
        # Valid concurrency field in request(default)
        response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "tcp"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("quotes", response.json())
    #----------------------end of R4

    # def test_quote_service_requested_number(self):
    #     # Valid request to quote service should return requested number of quotes
    #     response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "tcp", "concurrency": 4})
    #     self.assertEqual(response.status_code, 200)
    #     quotes = response.json().get("quotes")
    #     self.assertEqual(len(quotes), 4)

    # def test_concurrency_impact_on_pi_service(self):
    #     # Comparing processing time with different concurrency levels
    #     response_low_concurrency = requests.post(self.pi_url, json={**self.valid_user, "simulations": 1000, "concurrency": 1})
    #     response_high_concurrency = requests.post(self.pi_url, json={**self.valid_user, "simulations": 1000, "concurrency": 4})
    #     time_low = response_low_concurrency.json().get("processing_time")
    #     time_high = response_high_concurrency.json().get("processing_time")
    #     self.assertTrue(time_low > time_high)

    # def test_missing_or_invalid_field(self):
    #     # Missing field in pi service request
    #     response = requests.post(self.pi_url, json={**self.valid_user})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("error", response.json())

    #     # Invalid field in quote service request
    #     response = requests.post(self.quote_url, json={**self.valid_user, "protocol": "invalid"})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("error", response.json())


if __name__ == '__main__':
    unittest.main()
