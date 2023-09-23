from unittest import TestCase
from unittest import mock
from starlette.datastructures import QueryParams, Headers

from app.service.mock.mock_matcher import MockMatcher
from app.service.mock.mock_manager import MockManager
from app.service.mock.mock_manager import Mock


class TestMockMatcher(TestCase):

    def test_get_matching_mock__no_match(self) -> None:
        get_mocks_return_value = [
            Mock(
                name='test',
                method='GET',
                path='something_else'
            )
        ]
        with (
            mock.patch.object(MockManager, 'get_mocks', return_value=get_mocks_return_value),
            mock.patch.object(MockMatcher, '_mock_matches_request', return_value=False)
        ):
            actual = MockMatcher.get_matching_mock(
                method='GET',
                path='/something',
                query_params=QueryParams(
                    q='1'
                ),
                headers=Headers({
                    'Auth-Key': 'test'
                }),
                cookies={
                    'some': 'cookie'
                }
            )
            self.assertIsNone(actual)

    def test_get_matching_mock(self) -> None:
        get_mocks_return_value = [
            Mock(
                name='test',
                method='GET',
                path='something'
            )
        ]
        with (
            mock.patch.object(MockManager, 'get_mocks', return_value=get_mocks_return_value),
            mock.patch.object(MockMatcher, '_mock_matches_request', return_value=True)
        ):
            actual = MockMatcher.get_matching_mock(
                method='GET',
                path='/something',
                query_params=QueryParams(
                    q=1
                ),
                headers=Headers({
                    'Auth-Key': 'test'
                }),
                cookies={
                    'some': 'cookie'
                }
            )
            expected = get_mocks_return_value[0]
            self.assertEqual(expected, actual)

    def test_mock_matches_request__true(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_normalize_path', return_value='something'),
            mock.patch.object(MockMatcher, '_query_params_match', return_value=True),
            mock.patch.object(MockMatcher, '_headers_match', return_value=True),
            mock.patch.object(MockMatcher, '_cookies_match', return_value=True)
        ):
            mock_ = Mock(
                name='test',
                method='GET',
                path='something'
            )
            actual = MockMatcher._mock_matches_request(
                mock=mock_,
                method='GET',
                path='something',
                query_params=QueryParams(),
                headers=Headers(),
                cookies={}
            )
            self.assertTrue(actual)

    def test_mock_matches_request__wrong_path(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_normalize_path', return_value='something'),
            mock.patch.object(MockMatcher, '_query_params_match', return_value=True),
            mock.patch.object(MockMatcher, '_headers_match', return_value=True),
            mock.patch.object(MockMatcher, '_cookies_match', return_value=True)
        ):
            mock_ = Mock(
                name='test',
                method='POST',
                path='something'
            )
            actual = MockMatcher._mock_matches_request(
                mock=mock_,
                method='GET',
                path='something',
                query_params=QueryParams(),
                headers=Headers(),
                cookies={}
            )
            self.assertFalse(actual)

    def test_query_params_match__no_params(self) -> None:
        actual = MockMatcher._query_params_match(
            mock=Mock(
                name='test',
                method='GET',
                path='something'
            ),
            query_params=QueryParams(
                q='1'
            )
        )
        self.assertTrue(actual)

    def test_query_params_match__true(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_matches_regex', return_value=True)
        ):
            actual = MockMatcher._query_params_match(
                mock=Mock(
                    name='test',
                    method='GET',
                    path='something',
                    query_params={
                        'q': '1'
                    }
                ),
                query_params=QueryParams(
                    q='1'
                )
            )
            self.assertTrue(actual)

    def test_query_params_match__false(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_matches_regex', return_value=False)
        ):
            actual = MockMatcher._query_params_match(
                mock=Mock(
                    name='test',
                    method='GET',
                    path='something',
                    query_params={
                        'q': '1'
                    }
                ),
                query_params=QueryParams(
                    q='2'
                )
            )
            self.assertFalse(actual)

    def test_headers_match__no_headers(self) -> None:
        actual = MockMatcher._headers_match(
            mock=Mock(
                name='test',
                method='GET',
                path='something'
            ),
            headers=Headers({
                'q': '1'
            })
        )
        self.assertTrue(actual)

    def test_headers_match__true(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_matches_regex', return_value=True)
        ):
            actual = MockMatcher._headers_match(
                mock=Mock(
                    name='test',
                    method='GET',
                    path='something',
                    headers={
                        'q': '1'
                    }
                ),
                headers=Headers({
                    'q': '1'
                })
            )
            self.assertTrue(actual)

    def test_headers_match__false(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_matches_regex', return_value=False)
        ):
            actual = MockMatcher._headers_match(
                mock=Mock(
                    name='test',
                    method='GET',
                    path='something',
                    headers={
                        'q': '1'
                    }
                ),
                headers=Headers({
                    'q': '2'
                })
            )
            self.assertFalse(actual)

    def test_cookies_match__no_cookies(self) -> None:
        actual = MockMatcher._cookies_match(
            mock=Mock(
                name='test',
                method='GET',
                path='something'
            ),
            cookies={
                'q': '1'
            }
        )
        self.assertTrue(actual)

    def test_cookies_match__true(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_matches_regex', return_value=True)
        ):
            actual = MockMatcher._cookies_match(
                mock=Mock(
                    name='test',
                    method='GET',
                    path='something',
                    cookies={
                        'q': '1'
                    }
                ),
                cookies={
                    'q': '1'
                }
            )
            self.assertTrue(actual)

    def test_cookies_match__false(self) -> None:
        with (
            mock.patch.object(MockMatcher, '_matches_regex', return_value=False)
        ):
            actual = MockMatcher._cookies_match(
                mock=Mock(
                    name='test',
                    method='GET',
                    path='something',
                    cookies={
                        'q': '1'
                    }
                ),
                cookies={
                    'q': '2'
                }
            )
            self.assertFalse(actual)

    def test_matches_regex__optional_true(self) -> None:
        actual = MockMatcher._matches_regex(
            key='?q',
            value='^1.+$',
            actual=Headers({
                'q': '1a'
            })
        )
        self.assertTrue(actual)

    def test_matches_regex__optional_missing_true(self) -> None:
        actual = MockMatcher._matches_regex(
            key='?q',
            value='1',
            actual=QueryParams()
        )
        self.assertTrue(actual)

    def test_matches_regex__optional_false(self) -> None:
        actual = MockMatcher._matches_regex(
            key='?q',
            value='1',
            actual={
                'q': '2'
            }
        )
        self.assertFalse(actual)

    def test_matches_regex__required_true(self) -> None:
        actual = MockMatcher._matches_regex(
            key='q',
            value='^\\d+[a-z]+$',
            actual=QueryParams(
                q='123abc'
            )
        )
        self.assertTrue(actual)

    def test_matches_regex__required_false(self) -> None:
        actual = MockMatcher._matches_regex(
            key='q',
            value='1',
            actual=Headers({
                'q': '2'
            })
        )
        self.assertFalse(actual)

    def test_matches_regex__required_missing_false(self) -> None:
        actual = MockMatcher._matches_regex(
            key='q',
            value='1',
            actual={}
        )
        self.assertFalse(actual)

    def test_normalize_path__with_slash(self) -> None:
        actual = MockMatcher._normalize_path(path='/path')
        self.assertEqual('path', actual)

    def test_normalize_path__without_slash(self) -> None:
        actual = MockMatcher._normalize_path(path='path')
        self.assertEqual('path', actual)
