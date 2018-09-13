from alert.level import Level


class Strategy:

    # choose who should be called
    def getDes(self, level):
        return None

    def getCurrentLevel(self):
        return Level.EARTH
  
    def getAlert(self, level):
        return None

    def getContent(self, level):
        return None

    def before(self):
        pass

    def after(self):
        pass

    def shouldTrigger(self, level):
        return False

    def shouldFallback(self):
        return False
    
    def fallback(self):
        pass

    def onSuccess(self):
        pass
    
    def onFail(self):
        pass
    
    def _doRun(self):
        level = self.getCurrentLevel
        alert = self.getAlert(level)
        des = self.getAlert(level)
        content = self.getAlert(level)
        if self.shouldTrigger(level):
            alert.alert(level, des, content)
            if self.shouldFallback():
                self.fallback()
            self.onFail()
        else:
            self.onSuccess()


    def run(self):
        self.before()
        self._doRun()
        self.after()

