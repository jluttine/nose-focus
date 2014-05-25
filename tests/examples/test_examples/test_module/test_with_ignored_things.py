from nose_focus import focus_ignore
from unittest import TestCase

def test_not_ignored():
    assert True

@focus_ignore
def test_ignored():
    assert True

@focus_ignore
class IgnoredClass(TestCase):
    def test_blah(self):
        assert True

class IgnoredClassChild(IgnoredClass):
    def test_meh(self):
        assert True

