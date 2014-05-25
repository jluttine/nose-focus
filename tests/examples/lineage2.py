from tests.examples.lineage import AClass, ASubClass, ASubMixin

class BClass(object):
    def aMethod(self):
        pass

    def onlyBClass(self):
        pass

class BSubClassWithA(AClass):
    def aMethod(self):
        pass

    def onlyBSubClassWithA(self):
        pass

class BGrandClassWithA(ASubClass):
    def aMethod(self):
        pass

    def onlyBGrandClassWithA(self):
        pass

class BClassWithASubMixin(object, ASubMixin):
    def aMethod(self):
        pass
