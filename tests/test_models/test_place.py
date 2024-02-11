#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlaceInstantiation
    TestPlaceSave
    TestPlaceToDict
"""
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_name_is_public_class_attribute(self):
        place = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place))
        self.assertNotIn("name", place.__dict__)

    def test_two_places_unique_ids(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_two_places_different_created_at(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_two_places_different_updated_at(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = dt
        place_str = place.__str__()
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn("'created_at': " + dt_repr, place_str)
        self.assertIn("'updated_at': " + dt_repr, place_str)

    def test_args_unused(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUpClass(cls):
        cls.place = Place()

    @classmethod
    def tearDownClass(cls):
        del cls.place

    def test_one_save(self):
        first_updated_at = self.place.updated_at
        self.place.save()
        self.assertLess(first_updated_at, self.place.updated_at)

    def test_two_saves(self):
        first_updated_at = self.place.updated_at
        self.place.save()
        second_updated_at = self.place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        self.place.save()
        self.assertLess(second_updated_at, self.place.updated_at)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.place.save(None)

    def test_save_updates_file(self):
        self.place.save()
        place_id = "Place." + self.place.id
        with open("file.json", "r") as f:
            self.assertIn(place_id, f.read())


class TestPlaceToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def setUp(self):
        self.place = Place()

    def tearDown(self):
        del self.place

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.place.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", self.place.to_dict())
        self.assertIn("created_at", self.place.to_dict())
        self.assertIn("updated_at", self.place.to_dict())
        self.assertIn("__class__", self.place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        self.place.middle_name = "Holberton"
        self.place.my_number = 98
        self.assertEqual("Holberton", self.place.middle_name)
        self.assertIn("my_number", self.place.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        place_dict = self.place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        self.place.id = "123456"
        self.place.created_at = self.place.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.place.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.place.to_dict(), self.place.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.place.to_dict(None)


if __name__ == "__main__":
    unittest.main()
