from tests.examples.test_examples.test_module.test_focus_module import TestFocusClass

from unittest import TestCase

def test_nonfocus_function():
    assert True

class TestNonFocusClass(TestCase):
    def test_blah(self):
        assert True

class TestFocusClassChild(TestFocusClass):
    def test_stuff(self):
        assert True

