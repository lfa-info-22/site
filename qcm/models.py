from django.db import models

import random
import enum
import enumfields

from qcm.latex import evaluate_latex
from account.models import User

class QCMStatus(enum.Enum):
    ACTIVE = 0
    PRIVATE = 1

class QCMAnswer(models.Model):
    response = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

class QCMQuestion (models.Model):
    question = models.CharField(max_length=200)
    answers = models.ManyToManyField("QCMAnswer")
    
    def shuffle_answers (self) :
        data = list(self.answers.all())
        random.shuffle(data)
        return data

class QCM (models.Model):
    name = models.CharField(max_length=200)
    questions = models.ManyToManyField("QCMQuestion")
    status = enumfields.EnumField(QCMStatus)

    def shuffle_questions (self) :
        data = list(self.questions.all())
        random.shuffle(data)
        return data
    def enumerate_questions(self):
        return enumerate(self.questions.all(), 1)

    def get_status_orb_color(self):
        if self.status == QCMStatus.ACTIVE:
            return "bg-green-500"
        elif self.status == QCMStatus.PRIVATE:
            return "bg-indigo-500"
        return ""
    def get_status_name(self):
        if self.status == QCMStatus.ACTIVE:
            return "Active"
        elif self.status == QCMStatus.PRIVATE:
            return "Private"
        return ""


def build_qcm_from_latex_element(qcm_element, latex_element):
    if qcm_element == None:
        qcm_element = QCM.objects.create(name="QCM", status=QCMStatus.PRIVATE)
    qcm_element.questions.clear()

    for question_start in latex_element.query("{question}"):
        if question_start.name != "begin":
            continue

        bareme_element = question_start.parent.parent.query("bareme")[0]
        question_element = question_start.parent.elements[
            question_start.parent.elements.index(bareme_element) + 1
        ]
        qcm_question = qcm_element.questions.create(question=question_element)
        
        right_answers = question_start.parent.parent.query("bonne")
        false_answers = question_start.parent.parent.query("mauvaise")

        answers = right_answers + false_answers
        random.shuffle(answers)

        for answer in answers:
            qcm_question.answers.create(
                response=answer.parameters[0].elements[0],
                correct=answer.name == "bonne"
            )

class QCMUserResponse(models.Model):
    question  = models.ForeignKey("QCMQuestion", on_delete=models.CASCADE)
    answers   = models.ManyToManyField("QCMAnswer")

    user      = models.ForeignKey(User, on_delete=models.CASCADE)

    try_count = models.IntegerField()
    last_try  = models.DateTimeField()