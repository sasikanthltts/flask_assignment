import unittest
import requests
import json
from run import app

class TestApi(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

    def test_1_index(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        # print("test 1 completed")

    def test_1_app(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Hello, World!' in response.data)
        # print("test 2 completed")

    def test_get_all_users(self):
        tester = app.test_client(self)
        response = tester.get("/alluser")
        data = json.dumps(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_insert_data(self):
        insert_data = {
            "name":"sasi1",
            "gender":"male",
            "age": 27,
            "email":"sasi@ltts.com",
            "address":"hyd"
        }
        tester = app.test_client(self)
        response = tester.post("/users", json=insert_data)
        self.assertEqual(response.status_code, 200)
    
    # def test_insert_data_one(self):
    #     insert_data = {
    #         "name":"sasi1",
    #         "gender":"male",
    #         "age": 27,
    #         "email":"sasi@ltts.com"
    #     }
    #     tester = app.test_client(self)
    #     # response = tester.post("/users", json=insert_data)
    #     with self.assertRaises(KeyError):
    #         tester.post("/users", json=insert_data)


    
    
    def test_delete_field_by_id(self):
        tester = app.test_client(self)
        response = tester.delete("/delete/63218089cebce7df097198d5")
        self.assertEqual(response.status_code, 200)
        


if __name__ == "__main__":
    unittest.main()