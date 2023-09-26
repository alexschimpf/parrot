import re
from starlette.datastructures import QueryParams, Headers

from app.service.rule_manager import RuleManager, Rule


class RuleMatcher:

    @classmethod
    def get_matching_rule(
        cls,
        method: str,
        path: str,
        query_params: QueryParams,
        headers: Headers,
        cookies: dict[str, str]
    ) -> Rule | None:
        rules = RuleManager.get_rules()
        for rule in rules:
            if cls._rule_matches_request(
                rule=rule,
                method=method,
                path=path,
                query_params=query_params,
                headers=headers,
                cookies=cookies
            ):
                return rule

        return None

    @classmethod
    def _rule_matches_request(
        cls,
        rule: Rule,
        method: str,
        path: str,
        query_params: QueryParams,
        headers: Headers,
        cookies: dict[str, str]
    ) -> bool:
        rule.path = cls._normalize_path(path=rule.path)
        path = cls._normalize_path(path=path)

        return all((
            re.match(rule.path, path),
            rule.method.lower() == method.lower(),
            cls._query_params_match(rule=rule, query_params=query_params),
            cls._headers_match(rule=rule, headers=headers),
            cls._cookies_match(rule=rule, cookies=cookies)
        ))

    @classmethod
    def _query_params_match(cls, rule: Rule, query_params: QueryParams) -> bool:
        if not rule.query_params:
            return True

        for key, value in rule.query_params.items():
            if not cls._matches_regex(key=key, value=value, actual=query_params):
                return False

        return True

    @classmethod
    def _headers_match(cls, rule: Rule, headers: Headers) -> bool:
        if not rule.headers:
            return True

        for key, value in rule.headers.items():
            if not cls._matches_regex(key=key, value=value, actual=headers):
                return False

        return True

    @classmethod
    def _cookies_match(cls, rule: Rule, cookies: dict[str, str]) -> bool:
        if not rule.cookies:
            return True

        for key, value in rule.cookies.items():
            if not cls._matches_regex(key=key, value=value, actual=cookies):
                return False

        return True

    @staticmethod
    def _matches_regex(key: str, value: str, actual: QueryParams | Headers | dict[str, str]) -> bool:
        is_required = not key.startswith('?')
        if not is_required:
            key = key[1:]

        if key not in actual:
            return not is_required

        actual_value = actual[key]
        if not re.match(value, actual_value):
            return False

        return True

    @staticmethod
    def _normalize_path(path: str) -> str:
        if path.startswith('/'):
            path = path[1:]
        return path
