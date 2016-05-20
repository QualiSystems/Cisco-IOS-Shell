from cloudshell.shell.core.driver_bootstrap import DriverBootstrap

class CiscoIOSBootstrap(DriverBootstrap):

    def bindings(self, binder):
        """Binding for handler"""
        binder.bind_to_provider('handler', self._config.HANDLER_CLASS)
