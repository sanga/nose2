"""
Start a :func:`pdb.post_mortem` on errors and failures.

This plugin implements :func:`testOutcome` and will drop into pdb
whenever it sees a test outcome that includes exc_info.

It fires :func:`beforeInteraction` before launching pdb and
:func:`afterInteraction` after. Other plugins may implement
:func:`beforeInteraction` to return False and set event.handled to
prevent this plugin from launching pdb.

"""
import logging

from nose2 import events


__unittest = True
log = logging.getLogger(__name__)


class Debugger(events.Plugin):

    """Enter debugger on test error or failure"""

    configSection = 'debugger'
    commandLineSwitch = ('D', 'debugger', 'Enter debugger on test fail or error')

    def __init__(self):
        self.dbg = __import__('pdb')
        self.addArgument(self.overridedbg, None, 'debugger-to-use', 'use a debugger other than pdb (e.g. ipdb, pudb if they are installed)')
        self.errorsOnly = self.config.as_bool('errors-only', default=False)

    def overridedbg(self, dbg):
        self.dbg = __import__(dbg[0])

    def testOutcome(self, event):
        """Drop into debugger on unexpected errors or failures"""
        if not event.exc_info or event.expected:
            # skipped tests, unexpected successes, expected failures
            return

        value, tb = event.exc_info[1:]
        test = event.test
        if self.errorsOnly and isinstance(value, test.failureException):
            return
        evt = events.UserInteractionEvent()
        result = self.session.hooks.beforeInteraction(evt)
        try:
            if not result and evt.handled:
                log.warning(
                    "Skipping debugger for %s, user interaction not allowed", event)
                return
            self.dbg.post_mortem(tb)
        finally:
            self.session.hooks.afterInteraction(evt)
