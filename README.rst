Nose Focus
==========

This provides a nice little decorator and a nose-tests switch to make nose only
run the tests that you are focusing on right now.

.. image:: https://travis-ci.org/delfick/nose-focus.png?branch=master
    :target: https://travis-ci.org/delfick/nose-focus

Usage
-----

Just use the focus decorator in your tests:

.. code-block:: python

    from nose_focus import focus

    @focus
    def test_my_amazing_feature():
        assert_is_awesome(my_feature)

Or set it on your classes:

.. code-block:: python

    from nose_focus import focus

    @focus
    class MyTests(TestCase):
        [...]

Or if you also want to focus on subclasses:

.. code-block:: python

    @focus_all
    class MyTests(TestCase):
        [..]

    class OtherTests(MyTests):
        # Also part of the test because it's parent class has focus_all
        [..]

Or at the module level, set ``nose_focus`` to ``True``

.. code-block:: python

    nose_focus = True

    def test_my_other_amazing_feature():
        assert_great_things()

And use the switch when you run your tests:

.. code-block:: bash

    nosetests --with-focus

And the plugin will skip all the tests that we aren't focusing on or set to be
ignored.

You may also use nose_focus to run all your tests except those that are ignored.

.. code-block:: python

    from nose_focus import focus_ignore

    @focus_ignore
    def test_that_is_ignored():
        [..]

    def test_that_is_not_ignored():
        [..]

And use the ``--without-ignored`` to make it run all tests except those that
are ignored:

.. code-block:: bash

    nosetests --without-ignored

Api
---

nose_focus.focus(func)
    Sets ``nose_focus`` to ``True`` on ``func``

nose_focus.focus_all(kls)
    Sets ``nose_focus_all`` to ``True`` on ``kls``. The plugin looks for this
    attribute in the lineage of base classes for each method when determining
    to skip them or not.

nose_focus.focus_ignore(thing)
    Sets ``nose_focus_ignore`` to ``True`` on ``thing``. The plugin will look
    for this on each method and the lineage of base classes and will ignore the
    method if it finds it.

--with-focus nosetests switch
    Enables the plugin making it only run those tests that are set to focus
    and are not set to be ignored

--without-ignored nosetests switch
    Makes the plugin run all tests except those that are set to be ignored

How it works
------------

The plugin uses several ``want*`` hooks on a nose plugin  to only let
through methods that we want to focus on.

A method is ``focused`` if it or it's parent class has ``nose_focus`` set to
a Truthy value or if any class in the lineage of parent classes has
``nose_focus_all`` set to a Truthy value and nothing in the lineage
has ``nose_focus_ignore`` set to a Truthy value.

Installation
------------

Use pip!:

.. code-block:: bash

    pip install nose-focus

Or if you're developing it:

.. code-block:: bash

    pip install -e .
    pip install -e ".[tests]"

Tests
-----

To run the tests in this project, just use the helpful script:

.. code-block:: bash

    ./test.sh

Or run tox:

.. code-block:: bash

    tox

