class AClass(object):
    def aMethod(self):
        pass

    def onlyAClass(self):
        pass

class ASubClass(AClass):
    def aMethod(self):
        pass

    def bMethod(self):
        pass

    def onlySubClass(self):
        pass

class AGrandChildClass(ASubClass):
    def aMethod(self):
        pass

    def bMethod(self):
        pass

    def onlyGrandChildClass(self):
        pass

class AMixin:
    def aMethod(self):
        pass

    def bMethod(self):
        pass

    def onlyAMixin(self):
        pass

class BMixin:
    def aMethod(self):
        pass

    def bMethod(self):
        pass

    def onlyBMixin(self):
        pass

class ASubMixin(AMixin):
    def aMethod(self):
        pass

    def bMethod(self):
        pass

    def onlyASubMixin(self):
        pass

class AClassWithMixin(object, AMixin):
    def cMethod(self):
        pass

class AClassWithMixinAndOverride(object, AMixin):
    def aMethod(self):
        pass

class AClassWithSubMixin(object, ASubMixin):
    def cMethod(self):
        pass

class AClassWithSubMixinAndOverride(object, ASubMixin):
    def aMethod(self):
        pass

    def onlyAClassWithSubMixinAndOverride(self):
        pass

class AClassWithMultipleMixins(object, ASubMixin, BMixin):
    def aMethod(self):
        pass

class AClassWithEmbeddedClass(object):
    class EmbeddedClass(object):
        pass
AClassWithEmbeddedClass.EmbeddedClass.__embedded_class_parent__ = AClassWithEmbeddedClass

def aFunction(self):
    pass

