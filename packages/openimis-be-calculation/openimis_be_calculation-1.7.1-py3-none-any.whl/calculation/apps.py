import importlib
import inspect

from core.abs_calculation_rule import AbsCalculationRule
from django.apps import AppConfig


MODULE_NAME = "calculation"


DEFAULT_CFG = {
    "gql_query_calculation_rule_perms": ["153001"],
    "gql_mutation_update_calculation_rule_perms": ["153003"],
}


CALCULATION_RULES = []


def read_all_calculation_rules():
    """function to read all calculation rules"""
    for name, cls in inspect.getmembers(importlib.import_module("calculation.calculation_rule"), inspect.isclass):
        if 'calculation' in cls.__module__.split('.')[0]:
            CALCULATION_RULES.append(cls)
            cls.ready()


class CalculationConfig(AppConfig):
    name = MODULE_NAME

    gql_query_calculation_rule_perms = []
    gql_mutation_update_calculation_rule_perms = []

    def __load_config(self, cfg):
        for field in cfg:
            if hasattr(CalculationConfig, field):
                setattr(CalculationConfig, field, cfg[field])

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self.__load_config(cfg)
        read_all_calculation_rules()
