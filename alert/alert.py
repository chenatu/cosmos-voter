class Alert:

    def alert(self, level, des, content):
        self.before(level, des, content)
        self.doAlert(level, des, content)
        self.after(level, des, content)

    def before(self, level, des, content):
        pass

    def doAlert(self, level, des, content):
        pass

    def after(self, level, des, content):
        pass
