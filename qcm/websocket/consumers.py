
from lfainfo22.websocket.consumers import WSConsumer

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.template.loader import render_to_string

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

        if message_type == "CREATE_QUESTION":
            idx = message_data

            item = QCM.objects.filter(id=idx)
            if len(item) == 1:
                item = item[0]

                new_question = item.questions.create(question="Question")

                text = f"ADD_QUESTION_HTML: {idx}: " + render_to_string("qcm/editor/question.html", { "question": new_question, }, None)
                self.send(text)
        
        if message_type == "OPEN_QEDITOR":
            qcm_idx, question_idx = message_data.split(": ", 1)

            item = QCM.objects.filter(id=qcm_idx)
            if len(item) == 1:
                item = item[0]

                qitem = item.questions.filter(id=question_idx)
                if len(qitem) == 1:
                    qitem = qitem[0]

                    self.send("APPLY_QEDITOR: " + render_to_string("qcm/editor/question_editor.html", { "qcm": item, "question": qitem, }))

        if message_type == "MODIFY_QNAME":
            qcm_idx, question_idx, question_name = message_data.split(": ", 2)

            item = QCM.objects.filter(id=qcm_idx)
            if len(item) == 1:
                item = item[0]

                qitem = item.questions.filter(id=question_idx)
                if len(qitem) == 1:
                    qitem = qitem[0]

                    qitem.question = question_name
                    qitem.save()
        
        if message_type == "CREATE_ANSWER":
            qcm_idx, question_idx = message_data.split(": ", 1)

            item = QCM.objects.filter(id=qcm_idx)
            if len(item) == 1:
                item = item[0]

                qitem = item.questions.filter(id=question_idx)
                if len(qitem) == 1:
                    qitem = qitem[0]

                    qitem.answers.create(response="Answer", correct=False)

                    self.send("APPLY_QEDITOR: " + render_to_string("qcm/editor/question_editor.html", { "qcm": item, "question": qitem, }))
                    self.send(f"CHANGE_ANSWER_COUNT: {question_idx}: " + str(qitem.answers.count()))

        if message_type == "MODIFY_ARESP":
            qcm_idx, question_idx, answer_idx, answer_response = message_data.split(": ", 3)

            item = QCM.objects.filter(id=qcm_idx)
            if len(item) == 1:
                item = item[0]

                qitem = item.questions.filter(id=question_idx)
                if len(qitem) == 1:
                    qitem = qitem[0]

                    aitem = qitem.answers.filter(id=answer_idx)
                    if len(aitem) == 1:
                        aitem = aitem[0]
                        
                        aitem.response = answer_response
                        aitem.save()

        if message_type == "TOGGLE_ACORR":
            qcm_idx, question_idx, answer_idx = message_data.split(": ", 2)

            item = QCM.objects.filter(id=qcm_idx)
            if len(item) == 1:
                item = item[0]

                qitem = item.questions.filter(id=question_idx)
                if len(qitem) == 1:
                    qitem = qitem[0]

                    aitem = qitem.answers.filter(id=answer_idx)
                    if len(aitem) == 1:
                        aitem = aitem[0]
                        
                        aitem.correct = not aitem.correct
                        aitem.save()
        
        if message_type == "IMPORT_QCM":
            build_qcm_from_latex_element(None, evaluate_latex(message_data))
            self.send("REFRESH: /qcm/editor")

        return super().receive(text_data, bytes_data)

    def connect(self):
        self._user = self.scope['user']
        return super().connect()
