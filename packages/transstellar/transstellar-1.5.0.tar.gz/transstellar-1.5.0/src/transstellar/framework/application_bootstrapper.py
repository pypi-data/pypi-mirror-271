from transstellar.framework import Application


class ApplicationBootstrapper:
    def create_app(self, request, testrun_uid, options=None):
        if options is None:
            options = {}
        application = Application(request, testrun_uid, options)
        self.bootstrap(application)

        return application

    def bootstrap(self, app: Application):
        pass
