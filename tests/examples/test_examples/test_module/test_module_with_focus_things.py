from nose_focus import focus, focus_all
from unittest import TestCase

@focus
class TestFocusOneLayer(TestCase):
    def test_a_test(self):
        assert True

    def should_not_be_run(self):
        assert False

class TestFocusOneLayerChild(TestFocusOneLayer):
    def test_b_test(self):
        assert True

@focus_all
class TestFocusManyLayer(TestCase):
    def test_a_test(self):
        assert True

class TestFocusManyLayerChild(TestFocusManyLayer):
    def test_b_test(self):
        assert True

class TestFocusManyLayerGrandChild(TestFocusManyLayerChild):
    def test_c_test(self):
        assert True

@focus_all
def test_focus_all_function():
    assert True

@focus
def test_focused_function():
    assert True

@focus
def test_focused_function_two():
    assert True

def test_focused_function_brother():
    assert True

class TestFocusedFunctionBrother(TestCase):
    def test_blah(self):
        assert True

