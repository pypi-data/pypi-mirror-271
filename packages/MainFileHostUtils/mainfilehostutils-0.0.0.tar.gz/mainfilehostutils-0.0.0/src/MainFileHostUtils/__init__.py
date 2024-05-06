"""
\u0420\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A: MainPlay TG
https://t.me/MainPlay_InfoCh"""

__version_tuple__=(0,0,0)
__depends__={
  "required":[
    "MainShortcuts",
    ],
  "optional":[
    "requests",
    "MainHash",
    ],
  }
__scripts__=[]
__import_errors__={}
__all__=[]
try:
  from MainFileHostUtils.client import client
  __all__.append("client")
except Exception as e:
  __import_errors__["client"]=e
try:
  from MainFileHostUtils.server import server
  __all__.append("server")
except Exception as e:
  __import_errors__["server"]=e
__all__.sort()
__version__="{}.{}.{}".format(*__version_tuple__)
