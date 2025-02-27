from famapy.core.models import Configuration
from famapy.core.operations import Products

from famapy.metamodels.bdd_metamodel.models.bdd_model import BDDModel


class BDDProducts(Products):
    """It computes all the solutions of a BDD model.

    It also supports the computation of all solutions from a partial configuration.
    """

    def __init__(self, partial_configuration: Configuration = None) -> None:
        self.result: list[Configuration] = []
        self.bdd_model = None
        self.partial_configuration = partial_configuration

    def execute(self, model: BDDModel) -> 'BDDProducts':
        self.bdd_model = model
        self.result = products(self.bdd_model, self.partial_configuration)
        return self

    def get_result(self) -> list[Configuration]:
        return self.result

    def get_products(self) -> list[Configuration]:
        return products(self.bdd_model, self.partial_configuration)


def products(bdd_model: BDDModel, partial_config: Configuration = None) -> list[Configuration]:
    if partial_config is None:
        u_func = bdd_model.root
        care_vars = bdd_model.variables
        elements = {}
    else:
        values = dict(partial_config.elements.items())
        u_func = bdd_model.bdd.let(values, bdd_model.root)
        care_vars = set(bdd_model.variables) - values.keys()
        elements = partial_config.elements

    configs = []
    for assignment in bdd_model.bdd.pick_iter(u_func, care_vars=care_vars):
        features = {f: True for f in assignment.keys() if assignment[f]}
        features = features | elements
        configs.append(Configuration(features))
    return configs
