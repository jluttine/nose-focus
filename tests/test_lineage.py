# coding: spec

from noseOfYeti.tokeniser.support import noy_sup_setUp
from nose_focus.plugin import Lineage
from unittest import TestCase
import noseOfYeti

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

    describe "For an unbound method":
        it "Finds parent classes and modules":
            self.assertEqual(self.lineage.determine(lineage.AClass.onlyAClass), [lineage.AClass, tests.examples.lineage, tests.examples, tests])
            self.assertEqual(self.lineage.determine(lineage.AClass.aMethod), [lineage.AClass, tests.examples.lineage, tests.examples, tests])

        it "Finds grandparents":
            self.assertEqual(self.lineage.determine(lineage.ASubClass.onlySubClass), [lineage.ASubClass, tests.examples.lineage, tests.examples, tests, lineage.AClass])
            self.assertEqual(self.lineage.determine(lineage.ASubClass.aMethod), [lineage.ASubClass, tests.examples.lineage, tests.examples, tests, lineage.AClass])

            self.assertEqual(self.lineage.determine(lineage.AGrandChildClass.aMethod), [lineage.AGrandChildClass, tests.examples.lineage, tests.examples, tests, lineage.ASubClass, lineage.AClass])
            self.assertEqual(self.lineage.determine(lineage.AGrandChildClass.onlyGrandChildClass), [lineage.AGrandChildClass, tests.examples.lineage, tests.examples, tests, lineage.ASubClass, lineage.AClass])

            self.assertEqual(self.lineage.determine(lineage2.BSubClassWithA.aMethod), [lineage2.BSubClassWithA, tests.examples.lineage2, tests.examples, tests, lineage.AClass, tests.examples.lineage])
            self.assertEqual(self.lineage.determine(lineage2.BGrandClassWithA.aMethod), [lineage2.BGrandClassWithA, tests.examples.lineage2, tests.examples, tests, lineage.ASubClass, tests.examples.lineage, lineage.AClass])

        it "Works with mixins":
            self.assertEqual(self.lineage.determine(lineage.ASubMixin.aMethod), [lineage.ASubMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage.AClassWithMixin.aMethod), [lineage.AClassWithMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithMixin.onlyAMixin), [lineage.AClassWithMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage2.BClassWithASubMixin.aMethod), [lineage2.BClassWithASubMixin, tests.examples.lineage2, tests.examples, tests, lineage.ASubMixin, tests.examples.lineage, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage2.BClassWithASubMixin.onlyAMixin), [lineage2.BClassWithASubMixin, tests.examples.lineage2, tests.examples, tests, lineage.ASubMixin, tests.examples.lineage, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AMixin.onlyAMixin), [lineage.AMixin, tests.examples.lineage, tests.examples, tests])

            self.assertEqual(self.lineage.determine(lineage.AClassWithSubMixin.aMethod), [lineage.AClassWithSubMixin, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithMixinAndOverride.aMethod), [lineage.AClassWithMixinAndOverride, tests.examples.lineage, tests.examples, tests, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithSubMixinAndOverride.aMethod), [lineage.AClassWithSubMixinAndOverride, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithSubMixinAndOverride.onlyAClassWithSubMixinAndOverride), [lineage.AClassWithSubMixinAndOverride, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage.AClassWithMultipleMixins.aMethod), [lineage.AClassWithMultipleMixins, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin, lineage.BMixin])

    describe "For a bound method":
        it "Finds parent classes and modules":
            self.assertEqual(self.lineage.determine(lineage.AClass().onlyAClass), [lineage.AClass, tests.examples.lineage, tests.examples, tests])
            self.assertEqual(self.lineage.determine(lineage.AClass().aMethod), [lineage.AClass, tests.examples.lineage, tests.examples, tests])

        it "Finds grandparents":
            self.assertEqual(self.lineage.determine(lineage.ASubClass().onlySubClass), [lineage.ASubClass, tests.examples.lineage, tests.examples, tests, lineage.AClass])
            self.assertEqual(self.lineage.determine(lineage.ASubClass().aMethod), [lineage.ASubClass, tests.examples.lineage, tests.examples, tests, lineage.AClass])

            self.assertEqual(self.lineage.determine(lineage.AGrandChildClass().aMethod), [lineage.AGrandChildClass, tests.examples.lineage, tests.examples, tests, lineage.ASubClass, lineage.AClass])
            self.assertEqual(self.lineage.determine(lineage.AGrandChildClass().onlyGrandChildClass), [lineage.AGrandChildClass, tests.examples.lineage, tests.examples, tests, lineage.ASubClass, lineage.AClass])

            self.assertEqual(self.lineage.determine(lineage2.BSubClassWithA().aMethod), [lineage2.BSubClassWithA, tests.examples.lineage2, tests.examples, tests, lineage.AClass, tests.examples.lineage])
            self.assertEqual(self.lineage.determine(lineage2.BGrandClassWithA().aMethod), [lineage2.BGrandClassWithA, tests.examples.lineage2, tests.examples, tests, lineage.ASubClass, tests.examples.lineage, lineage.AClass])

        it "Works with mixins":
            self.assertEqual(self.lineage.determine(lineage.ASubMixin().aMethod), [lineage.ASubMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage.AClassWithMixin().aMethod), [lineage.AClassWithMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithMixin().onlyAMixin), [lineage.AClassWithMixin, tests.examples.lineage, tests.examples, tests, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage2.BClassWithASubMixin().aMethod), [lineage2.BClassWithASubMixin, tests.examples.lineage2, tests.examples, tests, lineage.ASubMixin, tests.examples.lineage, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage2.BClassWithASubMixin().onlyAMixin), [lineage2.BClassWithASubMixin, tests.examples.lineage2, tests.examples, tests, lineage.ASubMixin, tests.examples.lineage, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AMixin().onlyAMixin), [lineage.AMixin, tests.examples.lineage, tests.examples, tests])

            self.assertEqual(self.lineage.determine(lineage.AClassWithSubMixin().aMethod), [lineage.AClassWithSubMixin, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithMixinAndOverride().aMethod), [lineage.AClassWithMixinAndOverride, tests.examples.lineage, tests.examples, tests, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithSubMixinAndOverride().aMethod), [lineage.AClassWithSubMixinAndOverride, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin])
            self.assertEqual(self.lineage.determine(lineage.AClassWithSubMixinAndOverride().onlyAClassWithSubMixinAndOverride), [lineage.AClassWithSubMixinAndOverride, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin])

            self.assertEqual(self.lineage.determine(lineage.AClassWithMultipleMixins().aMethod), [lineage.AClassWithMultipleMixins, tests.examples.lineage, tests.examples, tests, lineage.ASubMixin, lineage.AMixin, lineage.BMixin])

    describe "For a function":
        it "Finds the modules":
            self.assertEqual(self.lineage.determine(lineage.aFunction), [tests.examples.lineage, tests.examples, tests])

