from noseOfYeti.tokeniser.support import noy_sup_setUp
from nose_focus.plugin import Lineage
from unittest import TestCase
import noseOfYeti
import nose
import six

from tests import examples
import tests

from tests.examples import lineage, lineage2

describe TestCase, "Finding lineage":
    before_each:
        self.lineage = Lineage()

    describe "For a built in":
        it "Finds no lineage":
            self.assertEqual(self.lineage.determine(len), [])
            self.assertEqual(self.lineage.determine(locals), [])

    describe "For a module":
        it "Finds parent modules":
            self.assertEqual(self.lineage.determine(examples), [tests])
            self.assertEqual(self.lineage.determine(noseOfYeti.tokeniser.support), [noseOfYeti.tokeniser, noseOfYeti])

    describe "For a class":
        it "Ignores object as a parent":
            self.assertEqual(self.lineage.determine(lineage.AClass), [tests.examples.lineage, tests.examples, tests])

        it "Finds parent classes and modules":
            self.assertEqual(self.lineage.determine(lineage.ASubClass), [tests.examples.lineage, tests.examples, tests, lineage.AClass])
            self.assertEqual(self.lineage.determine(lineage.AGrandChildClass), [tests.examples.lineage, tests.examples, tests, lineage.ASubClass, lineage.AClass])

        it "Finds Mixins":
            self.assertEqual(self.lineage.determine(lineage.AClassWithMixin), [tests.examples.lineage, tests.examples, tests, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithSubMixin), [tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithMultipleMixins), [tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin, lineage.BMixin])

        it "Finds parent classes with embedded classes if they have __embedded_class_parent__":
            self.assertEqual(self.lineage.determine(lineage.AClassWithEmbeddedClass.EmbeddedClass), [tests.examples.lineage, tests.examples, tests, lineage.AClassWithEmbeddedClass])

    describe "For a function":
        it "Finds the modules":
            self.assertEqual(self.lineage.determine(lineage.aFunction), [tests.examples.lineage, tests.examples, tests])

    describe "methods":
        def assert_finds(self, klses, methods, looking_for, instance_only=False, definition_only=False):
            """Assert that the methods on both the kls definition and kls instance finds the lineage we are looking for"""
            if not isinstance(klses, list) and not isinstance(klses, tuple):
                klses = [klses]

            if len(set(looking_for)) != len(looking_for):
                raise Exception("Looks like you have duplicates in looking_for...")

            if instance_only and definition_only:
                raise Exception("Doesn't make sense to call assert_finds with instance_only and definition_only both set to True")

            for method in methods:
                for kls in klses:
                    if not instance_only:
                        result = self.lineage.determine(getattr(kls, method))
                        if result != looking_for:
                            print("Determining {1} on {0} definition".format(kls, method))
                            print(result)
                            print('---')
                            print(looking_for)
                        self.assertEqual(result, looking_for)

                    if not definition_only:
                        result = self.lineage.determine(getattr(kls(), method))
                        if result != looking_for:
                            print("Determining {1} on {0} instance".format(kls, method))
                            print(result)
                            print('---')
                            print(looking_for)
                        self.assertEqual(result, looking_for)

        it "Finds parent classes and modules":
            self.assert_finds(lineage.AClass, ["onlyAClass", "aMethod"], [lineage.AClass, tests.examples.lineage, tests.examples, tests])

        describe "Inheritance":
            it "Finds the class the method is defined on":
                klses = [
                      lineage.AMixin, lineage.ASubMixin, lineage.AClassWithMixin, lineage.AClassWithSubMixin
                    , lineage2.BClassWithASubMixin, lineage.AClassWithMixinOverride, lineage.AClassWithSubMixinOverride, lineage2.BClassWithASubMixinOverride
                    , lineage2.BClassWithASubMixinOverride, lineage.AClassWithMultipleMixins
                    ]
                self.assert_finds(klses, ["onlyAMixin"]
                    , [lineage.AMixin, tests.examples.lineage, tests.examples, tests]
                    )

                klses = [
                      lineage.ASubMixin, lineage.AClassWithSubMixin, lineage2.BClassWithASubMixin, lineage.AClassWithSubMixinOverride
                    , lineage2.BClassWithASubMixinOverride, lineage.AClassWithMultipleMixins
                    ]
                self.assert_finds(klses, ["onlyASubMixin"]
                    , [lineage.ASubMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin]
                    )

                klses = [
                      lineage.AClass, lineage.ASubClass, lineage.ASubClassOverride, lineage.AGrandChildClass, lineage.AGrandChildClassOverride
                    , lineage2.BSubClass, lineage2.BSubClassOverride, lineage2.BGrandChildClass, lineage2.BGrandChildClassOverride
                    ]
                self.assert_finds(klses, ["onlyAClass"]
                    , [lineage.AClass, tests.examples.lineage, tests.examples, tests]
                    )

                klses = [lineage.ASubClass, lineage.AGrandChildClass, lineage.AGrandChildClassOverride]
                self.assert_finds(klses, ["onlyASubClass"]
                    , [lineage.ASubClass, tests.examples.lineage, tests.examples, tests, lineage.AClass]
                    )

                klses = [lineage2.BSubClass, lineage2.BGrandChildClass, lineage2.BGrandChildClassOverride]
                self.assert_finds(klses, ["onlyBSubClass"]
                    , [lineage2.BSubClass, tests.examples.lineage2, tests.examples, tests, lineage.AClass, tests.examples.lineage]
                    )

                self.assert_finds(lineage.AGrandChildClass, ["onlyAGrandChildClass"]
                    , [lineage.AGrandChildClass, tests.examples.lineage, tests.examples, tests, lineage.ASubClass, lineage.AClass]
                    )

            it "finds mixins from the method if the method is defined on the class we are getting it from":
                self.assert_finds(lineage.AMixin, ["onlyAMixin"]
                    , [lineage.AMixin, tests.examples.lineage, tests.examples, tests]
                    )

                self.assert_finds(lineage.ASubMixin, ["onlyASubMixin"]
                    , [lineage.ASubMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin]
                    )

                self.assert_finds(lineage.AClassWithMixin, ["onlyAClassWithMixin"]
                    , [lineage.AClassWithMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin]
                    )

                self.assert_finds(lineage.AClassWithSubMixin, ["onlyAClassWithSubMixin"]
                    , [lineage.AClassWithSubMixin, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin]
                    )

                self.assert_finds(lineage2.BClassWithASubMixin, ["onlyBClassWithASubMixin"]
                    , [lineage2.BClassWithASubMixin, tests.examples.lineage2, tests.examples, tests, lineage.ASubMixin, tests.examples.lineage, lineage.AMixin]
                    )

                self.assert_finds(lineage.ASubClassOverride, ["aMethod", "onlyASubClassOverride"]
                    , [lineage.ASubClassOverride, tests.examples.lineage, tests.examples, tests, lineage.AClass]
                    )

                self.assert_finds(lineage.AGrandChildClassOverride, ["aMethod", "onlyAGrandChildClassOverride"]
                    , [lineage.AGrandChildClassOverride, tests.examples.lineage, tests.examples, tests, lineage.ASubClass, lineage.AClass]
                    )

                self.assert_finds(lineage2.BSubClassOverride, ["aMethod", "onlyBSubClassOverride"]
                    , [lineage2.BSubClassOverride, tests.examples.lineage2, tests.examples, tests, lineage.AClass, tests.examples.lineage]
                    )

                self.assert_finds(lineage2.BGrandChildClassOverride, ["aMethod", "onlyBGrandChildClassOverride"]
                    , [lineage2.BGrandChildClassOverride, tests.examples.lineage2, tests.examples, tests, lineage2.BSubClass, lineage.AClass, tests.examples.lineage]
                    )

                self.assert_finds(lineage.AClassWithMixinOverride, ["aMethod", "onlyAClassWithMixinOverride"]
                    , [lineage.AClassWithMixinOverride, tests.examples.lineage, tests.examples, tests, lineage.AMixin]
                    )

                self.assert_finds(lineage.AClassWithSubMixinOverride, ["aMethod", "onlyAClassWithSubMixinOverride"]
                    , [lineage.AClassWithSubMixinOverride, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin]
                    )

                self.assert_finds(lineage2.BClassWithASubMixinOverride, ["aMethod", "onlyBClassWithASubMixinOverride"]
                    , [lineage2.BClassWithASubMixinOverride, tests.examples.lineage2, tests.examples, tests, lineage.ASubMixin, tests.examples.lineage, lineage.AMixin]
                    )

                self.assert_finds(lineage.AClassWithMultipleMixins, ["onlyAClassWithMultipleMixins"]
                    , [lineage.AClassWithMultipleMixins, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin, lineage.BMixin]
                    )
