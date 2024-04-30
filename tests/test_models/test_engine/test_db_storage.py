#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state = {"name": "Oromia"}
        new_state = State(**state)
        models.storage.new(new_state)
        models.storage.save()
        session = models.storage._DBStorage_session
        obj = session.query(State).all()
        self.assertTrue(len(obj) > 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state = {"name": "Amhara"}
        new_state = State(**state)
        models.storage.new(new_state)
        models.storage.save()

        session = models.storage._DBStorage__session
        data_found = session.query(State).filter_by(id=new_state.id).first()
        self.assertEqual(data_found.id, new_state.id)
        self.assertEqual(data_found.name, new_state.name)
        self.assertIsNotNone(data_found)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state = {"name": "Tigray"}
        new_state = State(**state)
        models.storage.save()

        session = models.storage._DBStorage_session
        data_found = session.query(State).filter_by(id=new_state.id).first()
        self.assertEqual(data_found.id, new_state.id)
        self.assertEqual(data_found.name, new_state.name)
        self.assertIsNotNone(data_found)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test method for to get data from db storage"""
        storage = models.storage()
        storage.reload()
        state = {"name": "south"}
        new_state = State(**state)
        data_found = storage.get(State, new_state.id)
        self.assertEqual(new_state, data_found)
        for_none = storage.get(State, "none_id")
        self.assertEqual(for_none, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test method for count the instance"""
        storage = models.storage()
        storage.reload()
        state = {"name": "Ethiopia"}
        new_state = State(**state)
        storage.new(new_state)
        city = {"name": "Addis", "state_id": new_state.id}
        new_city = City(**city)
        storage.new(new_city)
        storage.save()
        count_state = storage.count(State)
        self.assertEqual(count_state, len(storage.all(State)))
        count_all = storage.count()
        self.assertEqual(count_all, len(storage.all()))
