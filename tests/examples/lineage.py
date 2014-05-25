import six

class AClass(object):
    def aMethod(self):
        pass

    def onlyAClass(self):
        pass

class ASubClass(AClass):
    def onlyASubClass(self):
        pass

class ASubClassOverride(AClass):
    def aMethod(self):
        pass

    def onlyASubClassOverride(self):
        pass

class AGrandChildClass(ASubClass):
    def aMethod(self):
        pass

    def onlyAGrandChildClass(self):
        pass

class AGrandChildClassOverride(ASubClass):
    def aMethod(self):
        pass

    def onlyAGrandChildClassOverride(self):
        pass

class AMixin:
    def aMethod(self):
        pass

    def onlyAMixin(self):
        pass

class BMixin:
    def aMethod(self):
        pass

    def onlyBMixin(self):
        pass

class ASubMixin(AMixin):
    def aMethod(self):
        pass

    def onlyASubMixin(self):
        pass

if six.PY3:
    # With object as well, these become mro errors in python3
    # Because old style classes are now new style classes

    class AClassWithMixin(AMixin):
        def onlyAClassWithMixin(self):
            pass

    class AClassWithMixinOverride(AMixin):
        def aMethod(self):
            pass

        def onlyAClassWithMixinOverride(self):
            pass

    class AClassWithSubMixin(ASubMixin):
        def onlyAClassWithSubMixin(self):
            pass

    class AClassWithSubMixinOverride(ASubMixin):
        def aMethod(self):
            pass

        def onlyAClassWithSubMixinOverride(self):
            pass

    class AClassWithMultipleMixins(ASubMixin, BMixin):
        def onlyAClassWithMultipleMixins(self):
            pass
else:
    class AClassWithMixin(object, AMixin):
        def onlyAClassWithMixin(self):
            pass

    class AClassWithMixinOverride(object, AMixin):
        def aMethod(self):
            pass

        def onlyAClassWithMixinOverride(self):
            pass

    class AClassWithSubMixin(object, ASubMixin):
        def onlyAClassWithSubMixin(self):
            pass

    class AClassWithSubMixinOverride(object, ASubMixin):
        def aMethod(self):
            pass

        def onlyAClassWithSubMixinOverride(self):
            pass

    class AClassWithMultipleMixins(object, ASubMixin, BMixin):
        def onlyAClassWithMultipleMixins(self):
            pass

class AClassWithEmbeddedClass(object):
    class EmbeddedClass(object):
        pass
AClassWithEmbeddedClass.EmbeddedClass.__embedded_class_parent__ = AClassWithEmbeddedClass

def aFunction(self):
    pass

