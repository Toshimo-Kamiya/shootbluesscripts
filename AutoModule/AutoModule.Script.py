import shootblues
from shootblues.common import log
from shootblues.common.eve import SafeTimer, getFlagName, getNamesOfIDs, findModules, getModuleAttributes, getTypeAttributes, activateModule, canActivateModule, isModuleActive, runOnMainThread
from shootblues.common.service import forceStart, forceStop
import service
import json
import base
import uix
import blue
import foo
import math
import uthread

serviceInstance = None
serviceRunning = False

ModuleGroupNames = [
    "ECCM", "Sensor Booster", 
    "Damage Control"
]

class ModuleHelperSvc:
    def __init__(self):
        self.disabled = False
        self.__updateTimer = SafeTimer(250, self.updateModules)
    
    def updateModules(self):
        if self.disabled:
            self.__updateTimer = None
            return
        activeModules = findModules(groupNames=ModuleGroupNames)
        
        for moduleID, module in activeModules.items():
            if (canActivateModule(module) and (not isModuleActive(module))):
                activateModule(module)
    
    
def __load__():
    global serviceRunning, serviceInstance
    serviceRunning = True
    serviceInstance = forceStart("modulehelper", ModuleHelperSvc)

def __unload__():
    global serviceRunning, serviceInstance
    if serviceInstance:
        serviceInstance.disabled = True
        serviceInstance = None
    if serviceRunning:
        forceStop("modulehelper")
        serviceRunning = False