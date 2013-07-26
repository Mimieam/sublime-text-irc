# from .gntp.notifier import mini
# # Send a simple growl message with mostly default values
# from .gntp.notifier import mini
# # Send a simple growl message with mostly default values
# class IrcGntpClient(object):
    
#   mini("Here's a quick message", callback="http://github.com/")


# from .gntp.notifier import mini
# # Send a simple growl message with mostly default values
from .gntp.notifier import GrowlNotifier , mini

class IrcGntpClient(GrowlNotifier):

    def __init__(self,host='localhost',passw=None,p=23053,Icon=None):
        
        self.host = host
        growl = GrowlNotifier.__init__(self,
            applicationName='ST3-IRC', 
            notifications=["Updates","Messages"], 
            defaultNotifications=["Messages"], 
            applicationIcon=Icon, 
            hostname=host,
            password=passw,
            port=p)
        
        # self.growl = growl
        # print ('host: ',self.host,'growl:', growl , 'end')

    def notify(self,_title="New Msg",msg="u received a msg check out ST3 IRC",icon=None,_sticky=False,_priority=1):
        print ("sending Notify")
        print ('host: ',self.host,'growl:', self.growl , 'end')
        # Send one message
        try:
            self.growl.notify(
                    noteType = "Messages",
                    title = _title,
                    description = msg,
                    icon = None,
                    sticky = _sticky,
                    priority = _priority
            )
        except Exception as e :
            raise e
             
    def sendMini(self,msg="New Msg in ST3 IRC"):
        print ('sending MIni')
        mini(msg, callback="http://localhost.com:/")