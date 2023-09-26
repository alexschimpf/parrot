import json
import os
from pathlib import Path
from typing import Final, Any
from dataclasses import dataclass, asdict
from copy import deepcopy

from app import config


@dataclass
class Rule:
    name: str
    method: str
    path: str
    query_params: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    response_body: Any = None
    response_handler: str | None = None
    response_status: int | None = None
    response_headers: dict[str, str] | None = None


class RuleManager:

    _app_path: Final[str] = config.RULES_BASE_PATH
    _rules_dir: Final[str] = os.path.join(config.RULES_BASE_PATH, 'rules')
    _handlers_dir: Final[str] = os.path.join(config.RULES_BASE_PATH, 'handlers')
    _rules_config_file_path: Final[str] = os.path.join(config.RULES_BASE_PATH, 'rules.json')
    _rules_by_name: Final[dict[str, Rule]] = {}

    @classmethod
    def load_rules(cls) -> None:
        cls._load_rule_file(file_path=cls._rules_config_file_path, ignore_missing_file=True)

        rule_file_paths = (str(p.absolute()) for p in Path(cls._rules_dir).rglob('*.json'))
        for rule_file_path in rule_file_paths:
            cls._load_rule_file(file_path=rule_file_path, ignore_missing_file=False)

        if not os.path.exists(cls._app_path):
            os.mkdir(cls._app_path)

    @classmethod
    def add_or_update_rule(cls, rule: Rule, persist: bool = True) -> bool:
        existed = rule.name in cls._rules_by_name
        cls._rules_by_name[rule.name] = rule

        if persist:
            cls.save_to_disk()

        return existed

    @classmethod
    def remove_rule(cls, name: str, persist: bool = True) -> None:
        del cls._rules_by_name[name]

        if persist:
            cls.save_to_disk()

    @classmethod
    def get_rules_by_name(cls) -> dict[str, Rule]:
        return deepcopy(cls._rules_by_name)

    @classmethod
    def get_rules(cls) -> list[Rule]:
        rules_by_name = cls.get_rules_by_name()
        return list(dict(sorted(rules_by_name.items())).values())

    @classmethod
    def get_rule(cls, name: str) -> Rule | None:
        rules_by_name = cls.get_rules_by_name()
        return rules_by_name.get(name)

    @classmethod
    def clear_rules(cls) -> None:
        cls._rules_by_name.clear()
        cls.save_to_disk()

    @classmethod
    def save_to_disk(cls) -> None:
        with open(cls._rules_config_file_path, 'w+') as rules_config_fh:
            serialized_rules = json.dumps({
                name: asdict(rule)
                for name, rule in cls._rules_by_name.items()
            })
            rules_config_fh.write(serialized_rules)

    @classmethod
    def _load_rule_file(cls, file_path: str, ignore_missing_file: bool) -> None:
        if not os.path.exists(file_path) and ignore_missing_file:
            return

        with open(file_path, 'r') as rule_fh:
            rule_data_str = rule_fh.read()
            if rule_data_str:
                rule_data = json.loads(rule_data_str)
                for rule_name, rule in rule_data.items():
                    response_handler = rule.get('response_handler')
                    if response_handler and response_handler.startswith('file::'):
                        handler_file_path = os.path.join(cls._handlers_dir, response_handler[6:])
                        with open(handler_file_path, 'r') as response_handler_fh:
                            rule['response_handler'] = response_handler_fh.read()

                    cls._rules_by_name[rule_name] = Rule(**rule)
