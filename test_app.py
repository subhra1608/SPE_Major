import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict_endpoint_with_benign_data(self):
        input_data = {
            'worst perimeter': '179.10',
            'worst concave points': '0.2654',
            'mean concave points': '0.14740',
            'mean concavity': '0.31740',
            'worst radius': '0'
        }
        response = self.app.post('/predict', json=input_data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('prediction_text', data)

    def test_predict_endpoint_with_insufficient_data(self):
        input_data = {
    'worst perimeter': '0',
    'worst concave points': '0',
    'mean concave points': '0',
    'mean concavity': '0',
    'worst radius': ''
}

        response = self.app.post('/predict', json=input_data)
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
