import os
from rest_api_tester.test import TestCase
from rest_api_tester.runner import TestCaseRunner

from app.bootstrap import Bootstrap
from app.service.mock.mock_manager import MockManager

from tests.api.client import TestClient


class MocksRouteTestCase(TestCase):

    def setUp(self) -> None:
        MockManager.load_mocks()
        MockManager.clear_mocks()

        app = Bootstrap().run()
        test_client = TestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )

    def test_mocks_crud(self) -> None:
        try:
            self.get_mock_404()
            self.update_mock_404()
            self.delete_mock_404()

            self.create_mock()
            self.get_mock()
            self.update_mock()
            self.get_mocks()
        finally:
            self.delete_mock()

    def create_mock(self) -> None:
        self._run_test(test_name='create_mock')

    def update_mock(self) -> None:
        self._run_test(test_name='update_mock')

    def update_mock_404(self) -> None:
        self._run_test(test_name='update_mock_404')

    def delete_mock(self) -> None:
        self._run_test(test_name='delete_mock')

    def delete_mock_404(self) -> None:
        self._run_test(test_name='delete_mock_404')

    def get_mocks(self) -> None:
        self._run_test(test_name='get_mocks')

    def get_mock(self) -> None:
        self._run_test(test_name='get_mock')

    def get_mock_404(self) -> None:
        self._run_test(test_name='get_mock_404')

    def _run_test(self, test_name: str) -> None:
        result = self.runner.run(
            path_to_test_cases='test_mocks.json',
            test_name=test_name
        )
        self.verify_test_result(result=result)
