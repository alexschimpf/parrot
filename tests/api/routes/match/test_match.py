import os
from rest_api_tester.test import TestCase
from rest_api_tester.runner import TestCaseRunner

from app.bootstrap import Bootstrap
from app.service.mock.mock_manager import MockManager

from tests.api.client import TestClient


class MatchRouteTestCase(TestCase):

    def setUp(self) -> None:
        MockManager.load_mocks()
        MockManager.clear_mocks()

        app = Bootstrap().run()
        test_client = TestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '../mocks/__scenarios__')
        self.crud_runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )

        self.create_mock()
        self.create_mock_with_handler()

    def tearDown(self) -> None:
        self.delete_mock()
        self.delete_mock_with_handler()

    def test_match_none(self) -> None:
        self._run_test(test_name='match_none')

    def test_match_none2(self) -> None:
        self._run_test(test_name='match_none')

    def test_match(self) -> None:
        self._run_test(test_name='match')

    def test_match2(self) -> None:
        self._run_test(test_name='match2')

    def test_match_with_handler(self) -> None:
        self._run_test(test_name='match_with_handler')

    def create_mock(self) -> None:
        self._run_test(test_name='create_mock', is_crud=True)

    def create_mock_with_handler(self) -> None:
        self._run_test(test_name='create_mock_with_handler', is_crud=True)

    def delete_mock(self) -> None:
        self._run_test(test_name='delete_mock', is_crud=True)

    def delete_mock_with_handler(self) -> None:
        self._run_test(test_name='delete_mock_with_handler', is_crud=True)

    def _run_test(self, test_name: str, is_crud: bool = False) -> None:
        if is_crud:
            result = self.crud_runner.run(
                path_to_test_cases='test_mocks.json',
                test_name=test_name
            )
        else:
            result = self.runner.run(
                path_to_test_cases='test_match.json',
                test_name=test_name
            )
        self.verify_test_result(result=result)
