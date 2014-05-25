from nose_focus import focus_all
from unittest import TestCase

def test_things():
    assert True

class TestStuff(TestCase):
    def test_other(self):
        assert True

@focus_all
class TestWithFocusAllButIgnoredModule(TestCase):
    def test_things(self):
        assert True

