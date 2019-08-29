from django.apps import AppConfig


class PortalConfig(AppConfig):
    name = 'portal'


class LoadReceivers(AppConfig):
    name = 'portal'

    def ready(self):
        import paybooks.portal.signals

