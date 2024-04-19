#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
import models
from models import engine
from models.engine.file_storage import FileStorage
import json
import os
from models.state import State
from models.city import City

import models.user

User = models.user.User
BaseModel = models.base_model.BaseModel
FileStorage = engine.file_storage.FileStorage
storage = models.storage
F = "./dev/file.json"
storage_type = os.environ.get("HBNB_TYPE_STORAGE")


@unittest.skipIf(storage_type == "db", "skip if environ is db")
class TestBmFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print("\n\n.................................")
        print("...... Testing FileStorate ......")
        print("..... For FileStorage Class .....")
        print(".................................\n\n")

    def setUp(self):
        """initializes new storage object for testing"""
        self.storage = FileStorage()
        self.bm_obj = BaseModel()

    def test_instantiation(self):
        """... checks proper FileStorage instantiation"""
        self.assertIsInstance(self.storage, FileStorage)

    def test_to_dict(self):
        """... to_dict should return serializable dict object"""
        my_model_json = self.bm_obj.to_dict()
        actual = 1
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""

        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == "BaseModel":
                    actual = 1
        self.assertTrue(1 == actual)


class TestUserFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print("\n\n.................................")
        print("...... Testing FileStorage ......")
        print(".......... User  Class ..........")
        print(".................................\n\n")

    def setUp(self):
        """initializes new user for testing"""
        self.user = User()
        self.bm_obj = BaseModel()

    @unittest.skipIf(storage_type == "db", "skip if environ is db")
    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""

        self.user.save()
        self.assertTrue(os.path.isfile("file.json"))

    @unittest.skipIf(storage_type == "db", "skip if environ is db")
    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""

        self.user.save()
        u_id = self.user.id
        actual = 0
        with open("file.json", mode="r", encoding="utf-8") as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if u_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == "db", "skip if environ is db")
    def test_reload(self):
        """... checks proper usage of reload function"""

        self.bm_obj.save()
        u_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if u_id in k:
                actual = 1
        self.assertTrue(1 == actual)


@unittest.skipIf(storage_type == "db", "skip if environ is not db")
class TestStorageGet(unittest.TestCase):
    """
    Testing `get()` method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print("\n\n.................................")
        print("...... Testing Get() Method ......")
        print(".......... Place  Class ..........")
        print(".................................\n\n")

    def setUp(self):
        """
        setup method
        """
        self.state = models.state.State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """
        testing get() method
        :return: True if pass, False if not pass
        """

        print(self.state.id)
        result = storage.get(cls=State, id=self.state.id)

        self.assertIsInstance(result, models.state.State)

    def test_get_method_return(self):
        """
        testing get() method for id match
        :return: True if pass, false if not pass
        """
        result = storage.get(cls=State, id=str(self.state.id))

        self.assertEqual(self.state.id, result.id)

    def test_get_method_none(self):
        """
        testing get() method for None return
        :return: True if pass, false if not pass
        """
        result = storage.get(cls="State", id="doesnotexist")

        self.assertIsNone(result)


@unittest.skipIf(storage_type == "db", "skip if environ is not db")
class TestStorageCount(unittest.TestCase):
    """
    tests count() method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print("\n\n.................................")
        print("...... Testing Get() Method ......")
        print(".......... Place  Class ..........")
        print(".................................\n\n")

    def setup(self):
        """
        setup method
        """
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()

    def test_count_all(self):
        """
        testing counting all instances
        :return: True if pass, false if not pass
        """
        result = storage.count()

        self.assertEqual(len(storage.all()), result)

    def test_count_state(self):
        """
        testing counting state instances
        :return: True if pass, false if not pass
        """
        result = storage.count(cls=State)

        self.assertEqual(len(storage.all("State")), result)

    def test_count_city(self):
        """
        testing counting non existent
        :return: True if pass, false if not pass
        """
        result = storage.count(cls=City)

        self.assertEqual(
            int(1 if len(storage.all("City"))
                is None else len(storage.all("City"))),
            result,
        )


if __name__ == "__main__":
    unittest.main
