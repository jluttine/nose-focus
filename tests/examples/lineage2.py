from tests.examples.lineage import AClass, ASubMixin
import six

class BSubClass(AClass):
    def onlyBSubClass(self):
        pass

class BSubClassOverride(AClass):
    def aMethod(self):
        pass

    def onlyBSubClassOverride(self):
        pass

class BGrandChildClass(BSubClass):
    def onlyBGrandChildClass(self):
        pass

class BGrandChildClassOverride(BSubClass):
    def aMethod(self):
        pass

    def onlyBGrandChildClassOverride(self):
        pass

if six.PY3:
    # With object as well, this become mro errors in python3
    # Because old style classes are now new style classes

    class BClassWithASubMixin(ASubMixin):
        def onlyBClassWithASubMixin(self):
            pass

    class BClassWithASubMixinOverride(ASubMixin):
        def aMethod(self):
            pass

        def onlyBClassWithASubMixinOverride(self):
            pass
else:
    class BClassWithASubMixin(object, ASubMixin):
        def onlyBClassWithASubMixin(self):
            pass

    class BClassWithASubMixinOverride(object, ASubMixin):
        def aMethod(self):
            pass

        def onlyBClassWithASubMixinOverride(self):
            pass

