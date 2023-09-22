import json
import os
from pathlib import Path
from typing import Final, Any
from dataclasses import dataclass, asdict
from copy import deepcopy


@dataclass
class Mock:
    name: str
    method: str
    path: str
    query_params: dict[str, str] | None
    headers: dict[str, str] | None
    cookies: dict[str, str] | None
    response_body: Any
    response_handler: str | None
    response_status: int
    response_headers: dict[str, str] | None


class MockManager:

    _app_path: Final[str] = '/Users/alexschimpf/parrot'
    _mocks_dir: Final[str] = '/Users/alexschimpf/parrot/mocks'
    _handlers_dir: Final[str] = '/Users/alexschimpf/parrot/handlers'
    _mocks_config_file_path: Final[str] = '/Users/alexschimpf/parrot/mocks.json'
    _mocks_by_name: Final[dict[str, Mock]] = {}

    @classmethod
    def load_mocks(cls) -> None:
        cls._load_mock_file(file_path=cls._mocks_config_file_path, ignore_missing_file=True)

        mock_file_paths = map(lambda p: p.absolute(), Path(cls._mocks_dir).rglob('*.json'))
        for mock_file_path in mock_file_paths:
            cls._load_mock_file(file_path=mock_file_path, ignore_missing_file=False)

        if not os.path.exists(cls._app_path):
            os.mkdir(cls._app_path)

    @classmethod
    def add_or_update_mock(cls, mock: Mock, persist: bool = True) -> bool:
        existed = mock.name in cls._mocks_by_name
        cls._mocks_by_name[mock.name] = mock

        if persist:
            cls.save_to_disk()

        return existed

    @classmethod
    def remove_mock(cls, name: str, persist=True) -> None:
        del cls._mocks_by_name[name]

        if persist:
            cls.save_to_disk()

    @classmethod
    def get_mocks_by_name(cls) -> dict[str, Mock]:
        return deepcopy(cls._mocks_by_name)

    @classmethod
    def get_mocks(cls) -> list[Mock]:
        mocks_by_name = cls.get_mocks_by_name()
        return list(mocks_by_name.values())

    @classmethod
    def get_mock(cls, name: str) -> Mock:
        mocks_by_name = cls.get_mocks_by_name()
        return mocks_by_name.get(name)

    @classmethod
    def clear_mocks(cls) -> None:
        cls._mocks_by_name.clear()
        cls.save_to_disk()

    @classmethod
    def save_to_disk(cls) -> None:
        with open(cls._mocks_config_file_path, 'w+') as mock_config_fh:
            serialized_mocks = json.dumps({
                name: asdict(mock)
                for name, mock in cls._mocks_by_name.items()
            })
            mock_config_fh.write(serialized_mocks)

    @classmethod
    def _load_mock_file(cls, file_path, ignore_missing_file) -> None:
        if not os.path.exists(file_path) and ignore_missing_file:
            return

        with open(file_path, 'r') as mock_fh:
            raw_mock_data = mock_fh.read()
            if raw_mock_data:
                mock_data = json.loads(raw_mock_data)
                for mock_name, mock_item in mock_data.items():
                    response_handler = mock_item.get('response_handler')
                    if response_handler and response_handler.startswith('file::'):
                        handler_file_path = os.path.join(cls._handlers_dir, response_handler[6:])
                        with open(handler_file_path, 'r') as response_handler_fh:
                            mock_item['response_handler'] = response_handler_fh.read()

                    cls._mocks_by_name[mock_name] = Mock(**mock_item)
