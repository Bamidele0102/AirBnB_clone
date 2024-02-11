#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenityInstantiation
    TestAmenitySave
    TestAmenityToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amenity = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(amenity))
        self.assertNotIn("name", amenity.__dict__)

    def test_two_amenities_unique_ids(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_two_amenities_different_created_at(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_two_amenities_different_updated_at(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = dt
        amenity_str = amenity.__str__()
        self.assertIn("[Amenity] (123456)", amenity_str)
        self.assertIn("'id': '123456'", amenity_str)
        self.assertIn("'created_at': " + dt_repr, amenity_str)
        self.assertIn("'updated_at': " + dt_repr, amenity_str)

    def test_args_unused(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUpClass(cls):
        cls.amenity = Amenity()

    @classmethod
    def tearDownClass(cls):
        del cls.amenity

    def test_one_save(self):
        first_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(first_updated_at, self.amenity.updated_at)

    def test_two_saves(self):
        first_updated_at = self.amenity.updated_at
        self.amenity.save()
        second_updated_at = self.amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        self.amenity.save()
        self.assertLess(second_updated_at, self.amenity.updated_at)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.amenity.save(None)

    def test_save_updates_file(self):
        self.amenity.save()
        amenity_id = "Amenity." + self.amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amenity_id, f.read())


class TestAmenityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def setUp(self):
        self.amenity = Amenity()

    def tearDown(self):
        del self.amenity

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.amenity.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", self.amenity.to_dict())
        self.assertIn("created_at", self.amenity.to_dict())
        self.assertIn("updated_at", self.amenity.to_dict())
        self.assertIn("__class__", self.amenity.to_dict())

    def test_to_dict_contains_added_attributes(self):
        self.amenity.middle_name = "Holberton"
        self.amenity.my_number = 98
        self.assertEqual("Holberton", self.amenity.middle_name)
        self.assertIn("my_number", self.amenity.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        self.amenity.id = "123456"
        self.amenity.created_at = self.amenity.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.amenity.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.amenity.to_dict(), self.amenity.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()

