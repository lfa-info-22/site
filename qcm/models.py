from django.db import models

import random
import enum
import enumfields

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
    pass
