# coding: spec

from __future__ import print_function

from unittest import TestCase

import subprocess
import shlex
import fcntl
import time
import sys
import os
import re

this_folder = os.path.abspath(os.path.dirname(__file__))
test_folder = os.path.join(this_folder, "examples", "test_examples")

regexes = {
      "test_result": re.compile(r'((?P<name>[^ ]+) \((?P<home>[^\)]+)\)|(?P<full_test>[^ ]+))( ... )?ok')
    }

describe TestCase, "Running nose":
    def run_nose(self, other_args=""):
        """
        Run the example tests and return the names of the tests that ran

        Also make sure this doesn't hang indefinitely if things go wrong
        """
        output = []
        cmd = "nosetests {0} -v {1}".format(test_folder, other_args)
        args = shlex.split(cmd)

        process = subprocess.Popen(["which", "nosetests"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        if process.poll() is 0:
            location = process.stdout.read().strip().decode("utf8")
        else:
            assert False, "Couldn't discover the location of nosetests: {0}".format(process.stderr.read())
        ran = ' '.join([location] + args[1:])

        process = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        fl = fcntl.fcntl(process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(process.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        start = time.time()
        while True:
            if time.time() - start > 5:
                break
            if process.poll() is not None:
                break
            for nxt in self.read_non_blocking(process.stdout):
                output.append(nxt.decode("utf8"))
            time.sleep(0.01)

        if process.poll() is None:
            start = time.time()
            print("Ran: {0}".format(ran))
            print("Nosetests took longer than 5 seconds, asking it to terminate now", file=sys.stderr)
            process.terminate()

            while True:
                if time.time() - start > 5:
                    break
                if process.poll() is not None:
                    break
                for nxt in self.read_non_blocking(process.stdout):
                    output.append(nxt.decode("utf8"))
                time.sleep(0.01)

            if process.poll() is None:
                print("Nosetests took another 5 seconds after terminate, so sigkilling it now", file=sys.stderr)
                os.kill(process.pid, signal.SIGKILL)

        for nxt in self.read_non_blocking(process.stdout):
            output.append(nxt.decode("utf8"))

        if process.poll() is not 0:
            print('\n'.join(output))
            print("Ran: {0}".format(' '.join([location] + args[1:])))
            assert False, "Failed to run nosetests! Exited with code {0}".format(process.poll())

        tests = []
        output = [line.strip() for line in ''.join(output).split('\n')]

        for line in output:
            if not line.strip():
                break

            match = regexes["test_result"].match(line)
            if not match:
                print('\n'.join(output))
                assert False, "Expected all the lines to match a regex but this line didn't match: {0}".format(line)

            groups = match.groupdict()
            if groups.get("full_test"):
                tests.append(groups["full_test"])
            else:
                tests.append("{0}.{1}".format(groups["home"], groups["name"]))

        return ran, tests

    def read_non_blocking(self, stream):
        """Read from a non-blocking stream"""
        if stream:
            while True:
                nxt = ''
                try:
                    nxt = stream.readline()
                except IOError:
                    pass

                if nxt:
                    yield nxt
                else:
                    break

    def assert_expected_focus(self, expected, other_args=""):
        """Assert that only the tests we specify get run when we run nose with the specified args"""
        cmd, result = self.run_nose(other_args)
        if result != expected:
            print("Ran: {0}".format(cmd))
            print("Got:")
            print("\n".join(result))
            print("-" * 80)
            print("Expected:")
            print("\n".join(expected))
            print("=" * 80)
        self.assertEqual(result, expected)

    it "runs all the tests when run without nose_focus":
        expected = [
              "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.TestStuff.test_other"
            , "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.TestWithFocusAllButIgnoredModule.test_things"
            , "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.test_things"
            , "tests.examples.test_examples.test_ignored_module.test_things.TestStuff.test_other"
            , "tests.examples.test_examples.test_ignored_module.test_things.test_things"
            , "tests.examples.test_examples.test_module.test_focus_all_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_focus_all_module.test_focus_function"
            , "tests.examples.test_examples.test_module.test_focus_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_focus_module.test_focus_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayer.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_c_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayer.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayerChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayerChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusedFunctionBrother.test_blah"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focus_all_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function_two"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function_brother"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClassChild.test_blah"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClassChild.test_stuff"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestNonFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_non_focus_module.test_nonfocus_function"
            , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClass.test_blah"
            , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClassChild.test_blah"
            , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClassChild.test_meh"
            , "tests.examples.test_examples.test_module.test_with_ignored_things.test_not_ignored"
            , "tests.examples.test_examples.test_module.test_with_ignored_things.test_ignored"
            ]

        self.assert_expected_focus(expected)

    it "Runs all the tests except those that are ignored when run with --without-ignored":
        expected = [
            #   "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.TestStuff.test_other"
            # , "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.TestWithFocusAllButIgnoredModule.test_things"
            # , "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.test_things"
            # , "tests.examples.test_examples.test_ignored_module.test_things.TestStuff.test_other"
            # , "tests.examples.test_examples.test_ignored_module.test_things.test_things"
              "tests.examples.test_examples.test_module.test_focus_all_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_focus_all_module.test_focus_function"
            , "tests.examples.test_examples.test_module.test_focus_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_focus_module.test_focus_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayer.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_c_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayer.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayerChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayerChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusedFunctionBrother.test_blah"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focus_all_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function_two"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function_brother"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClassChild.test_blah"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClassChild.test_stuff"
            , "tests.examples.test_examples.test_module.test_non_focus_module.TestNonFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_non_focus_module.test_nonfocus_function"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClass.test_blah"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClassChild.test_blah"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClassChild.test_meh"
            , "tests.examples.test_examples.test_module.test_with_ignored_things.test_not_ignored"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.test_ignored"
            ]

        self.assert_expected_focus(expected, "--without-ignored")

    it "Runs only the focus tests if used with --with-focus":
        expected = [
            #   "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.TestStuff.test_other"
            # , "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.TestWithFocusAllButIgnoredModule.test_things"
            # , "tests.examples.test_examples.test_ignored_module.test_implicitly_ignored_module.test_stuff.test_things"
            # , "tests.examples.test_examples.test_ignored_module.test_things.TestStuff.test_other"
            # , "tests.examples.test_examples.test_ignored_module.test_things.test_things"
              "tests.examples.test_examples.test_module.test_focus_all_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_focus_all_module.test_focus_function"
            , "tests.examples.test_examples.test_module.test_focus_module.TestFocusClass.test_blah"
            , "tests.examples.test_examples.test_module.test_focus_module.test_focus_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayer.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_b_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusManyLayerGrandChild.test_c_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayer.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayerChild.test_a_test"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusOneLayerChild.test_b_test"
            # , "tests.examples.test_examples.test_module.test_module_with_focus_things.TestFocusedFunctionBrother.test_blah"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focus_all_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function"
            , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function_two"
            # , "tests.examples.test_examples.test_module.test_module_with_focus_things.test_focused_function_brother"
            # , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClass.test_blah"
            # , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClassChild.test_blah"
            # , "tests.examples.test_examples.test_module.test_non_focus_module.TestFocusClassChild.test_stuff"
            # , "tests.examples.test_examples.test_module.test_non_focus_module.TestNonFocusClass.test_blah"
            # , "tests.examples.test_examples.test_module.test_non_focus_module.test_nonfocus_function"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClass.test_blah"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClassChild.test_blah"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.IgnoredClassChild.test_meh"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.test_not_ignored"
            # , "tests.examples.test_examples.test_module.test_with_ignored_things.test_ignored"
            ]

        self.assert_expected_focus(expected, "--with-focus")

