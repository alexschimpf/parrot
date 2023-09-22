import os
from rest_api_tester.test import TestCase
from rest_api_tester.runner import TestCaseRunner

from app.bootstrap import Bootstrap

from tests.api.client import TestClient


class HealthRouteTestCase(TestCase):

    def setUp(self):
        app = Bootstrap().run()
        test_client = TestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir
        )
        super().setUp()

    def test_get_health__200(self):
        result = self.runner.run(
            path_to_test_cases='test_health.json',
            test_name='test_get_health__200'
        )
        self.verify_test_result(result=result)
