from unittest import TestCase
import requests


class TestAPI(TestCase):
    def setUp(self):
        self.url = "http://localhost:8080"
        self.created_id = None
        self.new_employee = {
             'first_name': "Ilia",
             'last_name': "Yartsev",
             'birth_date': "1989-04-09",
             'hire_date': "2021-11-01"
        }
        self.other_dude = {
             'first_name': "Other",
             'last_name': "Dude",
             'birth_date': "2005-03-29",
             'hire_date': "2024-02-15"
        }

    def test_create(self):
        """
        Testing Employees object creation
        """
        response = requests.post(self.url + "/employees/create", json=self.new_employee)
        self.assertEqual(response.status_code, 201)
        self.created_id = response.text

    def test_retrieve(self):
        """
        Testing Employees object retrieving by id
        """
        if not self.created_id:
            self.test_create()
        response = requests.get(self.url + "/employees/" + str(self.created_id))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ilia', response.text)

    def test_list(self):
        """
        Testing Employees objects listing
        """
        if not self.created_id:
            self.test_create()
        requests.post(self.url + "/employees/create", json=self.other_dude)
        response = requests.get(self.url + "/employees/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dude", response.text)
        self.assertIn("Ilia", response.text)

    def test_update(self):
        """
        Testing Employees object updating by id
        """
        if not self.created_id:
            self.test_create()
        response = requests.get(self.url + '/employees/' + str(self.created_id))
        self.assertIn("Ilia", response.text)
        response = requests.put(self.url + "/employees/" + str(self.created_id) + "/update", json=self.other_dude)
        self.assertEqual(response.status_code, 200)
        response = requests.get(self.url + '/employees/' + str(self.created_id))
        self.assertNotIn("Ilia", response.text)

    def test_delete(self):
        """
        Test deleting Employees object by id
        """
        response = requests.post(self.url + "/employees/create", json=self.other_dude)
        created_id = response.text
        self.assertEqual(response.status_code, 201)
        response = requests.get(self.url + "/employees/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dude", response.text)
        response = requests.delete(self.url + "/employees/" + created_id + "/delete")
        self.assertEqual(response.status_code, 200)
        response = requests.get(self.url + "/employees/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Dude", response.text)
