import unittest

from executorlib_core.inputcheck import (
    check_resource_dict,
    check_resource_dict_is_empty,
)


class TestInputCheck(unittest.TestCase):
    def test_check_resource_dict(self):
        def simple_function(resource_dict):
            return resource_dict

        with self.assertRaises(ValueError):
            check_resource_dict(function=simple_function)

    def test_check_resource_dict_is_empty(self):
        with self.assertRaises(ValueError):
            check_resource_dict_is_empty(resource_dict={"a": 1})
