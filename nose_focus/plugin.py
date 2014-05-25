from nose.plugins import Plugin
import __builtin__
import optparse
import inspect
import types
import sys

class Lineage(object):
    """Knows how to get the lineage of things"""
    def __init__(self):
        self.lineage = {}
        self.ignored = {}
        self.focused = {}
        self.focused_all = {}

    def determine(self, thing):
        """
        Get all the classes in the lineage of this method
        Memoize the results for each method and class as we go along
        """
        # from nose.tools import set_trace; set_trace()
        if repr(thing) not in self.lineage:
            lineage = []
            def add(thing):
                """Add something and it's lineage to lineage"""
                if thing not in lineage:
                    lineage.append(thing)
                    for determined in self.determine(thing):
                        if determined not in lineage:
                            lineage.append(determined)

            if type(thing) in (types.BuiltinMethodType, types.BuiltinFunctionType):
                pass

            elif type(thing) is types.ModuleType:
                name = thing.__name__
                if name.count(".") > 0:
                    parent = '.'.join(name.split('.')[:-1])
                    if parent in sys.modules:
                        add(sys.modules[parent])

            elif type(thing) in (types.UnboundMethodType, types.MethodType):
                parent = None
                if hasattr(thing, "im_class"):
                    parent = thing.im_class

                if parent:
                    add(parent)
            else:
                module = getattr(thing, "__module__", None)
                if isinstance(module, basestring):
                    module = sys.modules.get(module)

                if module and module is not __builtin__:
                    add(module)

                if type(thing) is not types.FunctionType:
                    klses = self.getmro(thing)

                    for kls in klses:
                        if kls and kls not in (thing, type, object):
                            add(kls)

            self.lineage[repr(thing)] = lineage
        return self.lineage[repr(thing)]

    def getmro(self, thing):
        """
        Get the mro list of a class and take into account custom __embedded_class_parent__ attribute.

        The __embedded_class_parent__ can be used by an embedded class to point at it's parent.
        """
        klses = list(inspect.getmro(thing))

        if hasattr(thing, "__embedded_class_parent__"):
            klses.extend(self.getmro(thing.__embedded_class_parent__))

        return klses

    def ignored(self, thing):
        """Ignored is thing or anything in lineage with nose_ignore set to true"""
        if thing not in self.ignored:
            self.ignored[thing] = False
            lineage = self.determine(thing)
            if getattr(lineage[0], "nose_focus_ignore", None) or (lineage and any(self.ignored(kls) for kls in lineage)):
                self.ignored[thing] = True
        return self.ignored[thing]

    def focused_all(self, thing):
        """Focused all is anything not ignored with the thing, or anything in it's lineage having focus_all set"""
        if thing not in self.focused_all:
            self.focused_all[thing] = False
            lineage = self.determine(thing)
            if not self.ignored(thing):
                if getattr(thing, "nose_focus_all", None) or (lineage and any(self.focused_all(kls) for kls in lineage)):
                    self.focused_all[thing] = True
        return self.focused_all[thing]

    def focused(self, thing):
        """Focused is not ignored, any parents focused due to focus_all logic, or this thing or parent has nose_focus set to Truthy"""
        if thing not in self.focused:
            self.focused[thing] = False
            lineage = self.determine(thing)
            if not self.ignored(thing):
                if lineage and any(self.focused_all(kls) for kls in lineage):
                    self.focused[thing] = True
                else:
                    parent = None
                    if lineage:
                        parent, lineage = lineage[0], lineage[1:]

                    if getattr(thing, "nose_focus", None) or (parent and getattr(parent, "nose_focus", None)):
                        self.focused[thing] = True
        return self.focused[thing]

class Plugin(Plugin):
    name = "nose_focus"

    def __init__(self, *args, **kwargs):
        self.lineage = Lineage()
        super(Plugin, self).__init__(*args, **kwargs)

    def wantMethod(self, method):
        """Only want methods that have nose_focus set to a truthy value"""
        if not self.enabled:
            return method

        if self.lineage.ignored(method):
            return

        if self.just_ignore:
            return method

        if self.lineage.focused(method):
            return method

    def options(self, parser, env={}):
        super(Plugin, self).options(parser, env)

        parser.add_option('--with-focus'
            , help    = 'Enable nose_focus'
            , action  = 'store_true'
            , dest    = 'only_focus'
            , default = False
            )

        parser.add_option('--without-ignored'
            , help    = 'Run all tests except those that are ignored'
            , action  = 'store_true'
            , dest    = 'just_ignore'
            , default = False
            )

    def configure(self, options, conf):
        super(Plugin, self).configure(options, conf)
        if options.enabled and options.just_ignore:
            raise optparse.OptionError("Please specify only one --with-focus or --without-ignored", "--with-focus")
        self.enabled = options.only_focus or options.just_ignore
        self.just_ignore = options.just_ignore

