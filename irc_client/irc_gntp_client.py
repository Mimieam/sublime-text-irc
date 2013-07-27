from .gntp.notifier import GrowlNotifier , mini

class IrcGntpClient(GrowlNotifier):
             
    def quickNotify(self, msg="New Msg in ST3 IRC", _title='ST3-IRC', sender="ST3-IRC",  callback=None):

        mini(msg, applicationName=_title, noteType="Message",
            title=sender, applicationIcon='.gntp/IRC.png', hostname='localhost',
            password=None, port=23053, sticky=False, priority=None,
            callback=None, notificationIcon='.gntp/IRC.png', identifier=None,
            notifierFactory=GrowlNotifier)