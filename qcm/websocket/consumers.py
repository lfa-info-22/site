
from lfainfo22.websocket.consumers import WSConsumer

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from qcm.models import *

class WSEditorConsumer(WSConsumer):
    def receive(self, text_data=None, bytes_data=None):
        if not self._user.is_staff:
            session = Session.objects.get(session_key=text_data)
            session_data = session.get_decoded()

            uid = session_data.get('_auth_user_id')
            self._user = User.objects.get(id=uid)
            return
        
        if not ": " in text_data:
            return

        message_type = text_data[:text_data.index(": ")]
        message_data = text_data[text_data.index(": ") + 2:]

        if message_type == "SET_QCM_NAME":
            idx, name = message_data.split(": ", 1)

            item = QCM.objects.filter(id=idx)
            if len(item) == 1:
                item = item[0]

                item.name = name
                item.save()
        
        if message_type == "TOGGLE_PRIVACY":
            idx = message_data

            item = QCM.objects.filter(id=idx)
            if len(item) == 1:
                item = item[0]

                item.status = QCMStatus.ACTIVE if item.status == QCMStatus.PRIVATE else QCMStatus.PRIVATE
                item.save()

        return super().receive(text_data, bytes_data)

    def connect(self):
        self._user = self.scope['user']
        return super().connect()
