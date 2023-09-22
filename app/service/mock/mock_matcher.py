import re
from starlette.datastructures import QueryParams, Headers

from app.service.mock.mock_manager import MockManager, Mock


class MockMatcher:

    @classmethod
    def get_matching_mock(
        cls,
        method: str,
        path: str,
        query_params: QueryParams,
        headers: Headers,
        cookies: dict[str, str]
    ) -> Mock | None:
        mocks = MockManager.get_mocks()
        for mock in mocks:
            if cls._mock_matches_request(
                mock=mock,
                method=method,
                path=path,
                query_params=query_params,
                headers=headers,
                cookies=cookies
            ):
                return mock

        return None

    @classmethod
    def _mock_matches_request(
        cls,
        mock: Mock,
        method: str,
        path: str,
        query_params: QueryParams,
        headers: Headers,
        cookies: dict[str, str]
    ) -> bool:
        return all((
            mock.path == path,
            mock.method.lower() == method.lower(),
            cls._query_params_match(mock=mock, query_params=query_params),
            cls._headers_match(mock=mock, headers=headers),
            cls._cookies_match(mock=mock, cookies=cookies)
        ))

    @classmethod
    def _query_params_match(cls, mock: Mock, query_params: QueryParams) -> bool:
        if not mock.query_params:
            return True

        for key, value in mock.query_params.items():
            if not cls._matches_regex(key=key, value=value, actual=query_params):
                return False

        return True

    @classmethod
    def _headers_match(cls, mock: Mock, headers: Headers) -> bool:
        if not mock.headers:
            return True

        for key, value in mock.headers.items():
            if not cls._matches_regex(key=key, value=value, actual=headers):
                return False

        return True

    @classmethod
    def _cookies_match(cls, mock: Mock, cookies: dict[str, str]) -> bool:
        if not mock.cookies:
            return True

        for key, value in mock.cookies.items():
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
