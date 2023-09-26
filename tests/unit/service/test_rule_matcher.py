from unittest import TestCase
from unittest import mock
from starlette.datastructures import QueryParams, Headers

from app.service.rule_matcher import RuleMatcher
from app.service.rule_manager import RuleManager, Rule


class TestRuleMatcher(TestCase):

    def test_get_matching_rule__no_match(self) -> None:
        get_rules_return_value = [
            Rule(
                name='test',
                method='GET',
                path='something_else'
            )
        ]
        with (
            mock.patch.object(RuleManager, 'get_rules', return_value=get_rules_return_value),
            mock.patch.object(RuleMatcher, '_rule_matches_request', return_value=False)
        ):
            actual = RuleMatcher.get_matching_rule(
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

    def test_get_matching_rule(self) -> None:
        get_rules_return_value = [
            Rule(
                name='test',
                method='GET',
                path='something'
            )
        ]
        with (
            mock.patch.object(RuleManager, 'get_rules', return_value=get_rules_return_value),
            mock.patch.object(RuleMatcher, '_rule_matches_request', return_value=True)
        ):
            actual = RuleMatcher.get_matching_rule(
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
            expected = get_rules_return_value[0]
            self.assertEqual(expected, actual)

    def test_rule_matches_request__true(self) -> None:
        with (
            mock.patch.object(RuleMatcher, '_normalize_path', return_value='something'),
            mock.patch.object(RuleMatcher, '_query_params_match', return_value=True),
            mock.patch.object(RuleMatcher, '_headers_match', return_value=True),
            mock.patch.object(RuleMatcher, '_cookies_match', return_value=True)
        ):
            rule = Rule(
                name='test',
                method='GET',
                path='something'
            )
            actual = RuleMatcher._rule_matches_request(
                rule=rule,
                method='GET',
                path='something',
                query_params=QueryParams(),
                headers=Headers(),
                cookies={}
            )
            self.assertTrue(actual)

    def test_rule_matches_request__wrong_path(self) -> None:
        with (
            mock.patch.object(RuleMatcher, '_normalize_path', return_value='something'),
            mock.patch.object(RuleMatcher, '_query_params_match', return_value=True),
            mock.patch.object(RuleMatcher, '_headers_match', return_value=True),
            mock.patch.object(RuleMatcher, '_cookies_match', return_value=True)
        ):
            rule = Rule(
                name='test',
                method='POST',
                path='something'
            )
            actual = RuleMatcher._rule_matches_request(
                rule=rule,
                method='GET',
                path='something',
                query_params=QueryParams(),
                headers=Headers(),
                cookies={}
            )
            self.assertFalse(actual)

    def test_query_params_match__no_params(self) -> None:
        actual = RuleMatcher._query_params_match(
            rule=Rule(
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
            mock.patch.object(RuleMatcher, '_matches_regex', return_value=True)
        ):
            actual = RuleMatcher._query_params_match(
                rule=Rule(
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
            mock.patch.object(RuleMatcher, '_matches_regex', return_value=False)
        ):
            actual = RuleMatcher._query_params_match(
                rule=Rule(
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
        actual = RuleMatcher._headers_match(
            rule=Rule(
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
            mock.patch.object(RuleMatcher, '_matches_regex', return_value=True)
        ):
            actual = RuleMatcher._headers_match(
                rule=Rule(
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
            mock.patch.object(RuleMatcher, '_matches_regex', return_value=False)
        ):
            actual = RuleMatcher._headers_match(
                rule=Rule(
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
        actual = RuleMatcher._cookies_match(
            rule=Rule(
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
            mock.patch.object(RuleMatcher, '_matches_regex', return_value=True)
        ):
            actual = RuleMatcher._cookies_match(
                rule=Rule(
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
            mock.patch.object(RuleMatcher, '_matches_regex', return_value=False)
        ):
            actual = RuleMatcher._cookies_match(
                rule=Rule(
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
        actual = RuleMatcher._matches_regex(
            key='?q',
            value='^1.+$',
            actual=Headers({
                'q': '1a'
            })
        )
        self.assertTrue(actual)

    def test_matches_regex__optional_missing_true(self) -> None:
        actual = RuleMatcher._matches_regex(
            key='?q',
            value='1',
            actual=QueryParams()
        )
        self.assertTrue(actual)

    def test_matches_regex__optional_false(self) -> None:
        actual = RuleMatcher._matches_regex(
            key='?q',
            value='1',
            actual={
                'q': '2'
            }
        )
        self.assertFalse(actual)

    def test_matches_regex__required_true(self) -> None:
        actual = RuleMatcher._matches_regex(
            key='q',
            value='^\\d+[a-z]+$',
            actual=QueryParams(
                q='123abc'
            )
        )
        self.assertTrue(actual)

    def test_matches_regex__required_false(self) -> None:
        actual = RuleMatcher._matches_regex(
            key='q',
            value='1',
            actual=Headers({
                'q': '2'
            })
        )
        self.assertFalse(actual)

    def test_matches_regex__required_missing_false(self) -> None:
        actual = RuleMatcher._matches_regex(
            key='q',
            value='1',
            actual={}
        )
        self.assertFalse(actual)

    def test_normalize_path__with_slash(self) -> None:
        actual = RuleMatcher._normalize_path(path='/path')
        self.assertEqual('path', actual)

    def test_normalize_path__without_slash(self) -> None:
        actual = RuleMatcher._normalize_path(path='path')
        self.assertEqual('path', actual)
