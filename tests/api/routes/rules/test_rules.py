import os
from rest_api_tester.test import TestCase
from rest_api_tester.runner import TestCaseRunner

from app.bootstrap import Bootstrap
from app.service.rule_manager import RuleManager

from tests.api.client import TestClient


class RulesRouteTestCase(TestCase):

    def setUp(self) -> None:
        RuleManager.load_rules()
        RuleManager.clear_rules()

        app = Bootstrap().run()
        test_client = TestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )

    def test_rules_crud(self) -> None:
        try:
            self.get_rule_404()
            self.update_rule_404()
            self.delete_rule_404()

            self.create_rule()
            self.get_rule()
            self.update_rule()
            self.get_rules()
        finally:
            self.delete_rule()

    def create_rule(self) -> None:
        self._run_test(test_name='create_rule')

    def update_rule(self) -> None:
        self._run_test(test_name='update_rule')

    def update_rule_404(self) -> None:
        self._run_test(test_name='update_rule_404')

    def delete_rule(self) -> None:
        self._run_test(test_name='delete_rule')

    def delete_rule_404(self) -> None:
        self._run_test(test_name='delete_rule_404')

    def get_rules(self) -> None:
        self._run_test(test_name='get_rules')

    def get_rule(self) -> None:
        self._run_test(test_name='get_rule')

    def get_rule_404(self) -> None:
        self._run_test(test_name='get_rule_404')

    def _run_test(self, test_name: str) -> None:
        result = self.runner.run(
            path_to_test_cases='test_rules.json',
            test_name=test_name
        )
        self.verify_test_result(result=result)
