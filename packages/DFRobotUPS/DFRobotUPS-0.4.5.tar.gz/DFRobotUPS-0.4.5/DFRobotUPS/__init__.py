# DFRobotUPS.__init__



__version__ = "0.4.5"



from .ups import (DFRobotUPS, DEFAULT_ADDR, DEFAULT_BUS, PID, DETECT_OK,
                  DETECT_NOSMBUS, DETECT_NODEVICE, DETECT_INVALIDPID)



__all__ = [
    "DFRobotUPS",
    "DEFAULT_ADDR",
    "DEFAULT_BUS",
    "PID",
    "DETECT_OK",
    "DETECT_NOSMBUS",
    "DETECT_NODEVICE",
    "DETECT_INVALIDPID",
]
