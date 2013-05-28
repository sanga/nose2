from nose2.plugins.debugger import Debugger
from nose2.tests._common import FunctionalTestCase

class LoggingDebugger(Debugger):
    def importer(self, mod):
        print mod
        Debugger.importer(mod)

Debugger = LoggingDebugger

class DebuggerPluginTestRuns(FunctionalTestCase):
    def test_correctly_uses_configured_debugger(self):
        self.runIn('scenario/tests_in_package',
                  'pkg1.test.test_things.SomeTests.test_failed',
                  '-D',
                  '--debugger-to-use=ipdb')

    def test_defaults_to_pdb(self):
        self.runIn('scenario/tests_in_package',
                  'pkg1.test.test_things.SomeTests.test_failed',
                  '-D')

    def test_throws_reasonable_error_on_import_failure(self):
        self.runIn('scenario/tests_in_package',
                  'pkg1.test.test_things.SomeTests.test_failed',
                  '-D',
                  '--debugger-to-use=imnothere')
