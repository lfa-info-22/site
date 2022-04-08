from django.test import TestCase
from lfainfo22.tests import ClientTestCase
from train.views import DeleteTrainingPlan, GetAllTrainingPlans, GetTimedExercices
from train.models import *

class GetAllTrainingPlansTest(ClientTestCase):
    VIEW = GetAllTrainingPlans()

    ROUTE = f"/api/v{VIEW.VERSION}/{VIEW.APPLICATION}/{VIEW.ROUTE}"

    def setUp(self):
        super().setUp()

        exercice = Exercice.objects.create(name="EX")
        texercice = TimedExercice.objects.create(exercice=exercice, minutes=10, seconds=10)

        for i in range(self.VIEW.PAGINATION + 1):
            plan = TrainingPlan.objects.create(name="PLAN" + str(i), user=self.user)
            plan.timed_exercices.add(texercice)
        plan = TrainingPlan.objects.create(name="PLAN", user=self.staff_user)
        plan.timed_exercices.add(texercice)

    def test_can_access(self):
        self.send_lambda_request(self.ROUTE, {})
    def test_value(self):
        resp = self.client.get(self.ROUTE, {})
        json = resp.json()

        idx = self.VIEW.PAGINATION + 1
        for data in json['data']:
            self.assertEqual(data, { 'id': idx, 'name': f"PLAN{idx-1}", 'exercices':[1]})
            idx -= 1
        
        resp = self.staff_client.get(self.ROUTE, {})
        json = resp.json()
        self.assertEqual(json, {'data': [{'id': self.VIEW.PAGINATION + 2, 'name': 'PLAN', 'exercices': [1]}], 'status': 200})
    def test_related(self):
        resp = self.client.get(self.ROUTE + f"?related={self.staff_user.username}", {})
        json = resp.json()
        self.assertEqual(json, {'data': [{'id': self.VIEW.PAGINATION + 2, 'name': 'PLAN', 'exercices': [1]}], 'status': 200})
    def test_last_seen(self):
        resp = self.client.get(self.ROUTE + '?last_seen=' + str(self.VIEW.PAGINATION + 1), {})
        json = resp.json()

        idx = self.VIEW.PAGINATION
        for data in json['data']:
            self.assertEqual(data, { 'id': idx, 'name': f"PLAN{idx-1}", 'exercices':[1]})
            idx -= 1

class GetTimedExerciceTest(ClientTestCase):
    VIEW = GetTimedExercices()

    ROUTE = f"/api/v{VIEW.VERSION}/{VIEW.APPLICATION}/{VIEW.ROUTE}"

    def setUp(self):
        super().setUp()

        exercice = Exercice.objects.create(name="EX")
        texercice = TimedExercice.objects.create(exercice=exercice, minutes=10, seconds=10)

        self.FROUTE = self.ROUTE.replace('<int:id>', str(texercice.id + 1))
        self.ROUTE  = self.ROUTE.replace('<int:id>', str(texercice.id))
    def test_access(self):
        self.send_request(self.ROUTE, {})
        self.send_request(self.FROUTE, {}, 404, 404, 404)
    def test_value(self):
        resp = self.client.get(self.ROUTE, {})
        json = resp.json()

        self.assertEqual(json, {'data': {'exercice': 'EX', 'minutes': 10, 'seconds': 10}, 'status': 200})

class DeleteTrainingPlanTest(ClientTestCase):
    VIEW = DeleteTrainingPlan()

    ROUTE = f"/api/v{VIEW.VERSION}/{VIEW.APPLICATION}/{VIEW.ROUTE}"

    def setUp(self):
        super().setUp()

        exercice = Exercice.objects.create(name="EX")
        texercice = TimedExercice.objects.create(exercice=exercice, minutes=10, seconds=10)

        plan = TrainingPlan.objects.create(name="PLAN", user=self.staff_user)
        plan.timed_exercices.add(texercice)
    
    def test_can_access(self):
        rROUTE  = self.ROUTE.replace("<int:id>", "1")
        response = self.staff_client.get(rROUTE)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/train/schedule/")
        self.assertEqual(TrainingPlan.objects.count(), 0)
    def test_can_other_access(self):
        rROUTE  = self.ROUTE.replace("<int:id>", "1")
        response = self.client.get(rROUTE)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(TrainingPlan.objects.count(), 1)

        response = self.anonymous_client.get(rROUTE)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(TrainingPlan.objects.count(), 1)
    def test_next(self):
        rROUTE  = self.ROUTE.replace("<int:id>", "1")
        response = self.staff_client.get(rROUTE, { "next": "/next/" })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/next/")
    def test_json_resp(self):
        rROUTE  = self.ROUTE.replace("<int:id>", "1")
        response = self.staff_client.get(rROUTE, { "json_resp": "True" })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), { "status": 200, "data": True})
    def test_false_input(self):
        rROUTE  = self.ROUTE.replace("<int:id>", "0")
        response = self.staff_client.get(rROUTE)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(TrainingPlan.objects.count(), 1)