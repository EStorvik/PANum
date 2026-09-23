import pytest

from panum import FEMHandler


class _DummyBaseHandler(FEMHandler):
    """Test helper that bypasses dolfinx-dependent function creation."""

    def __init__(self) -> None:
        self.stages = 1
        super().__init__()

    def generate_functions(self) -> None:
        self.xi = object()
        self.eta = object()
        self.xi_stages = [object()]
        self.xi_old = self.xi_stages[0]


class _MissingMappingsHandler(_DummyBaseHandler):
    def define_fields(self) -> None:
        self.us = {0: object()}


class _KeyMismatchHandler(_DummyBaseHandler):
    def define_fields(self) -> None:
        self.us = {0: object()}
        self.vs = {0: object()}
        self.eta_us = {1: object()}
        self.eta_vs = {0: object()}
        self.us_old = {0: object()}
        self.vs_old = {0: object()}
        self.us_stages = [{0: object()}]
        self.vs_stages = [{0: object()}]


class _ValidHandler(_DummyBaseHandler):
    def define_fields(self) -> None:
        self.us = {0: object()}
        self.vs = {0: object()}
        self.eta_us = {0: object()}
        self.eta_vs = {0: object()}
        self.us_old = {0: object()}
        self.vs_old = {0: object()}
        self.us_stages = [{0: object()}]
        self.vs_stages = [{0: object()}]


def test_femhandler_contract_missing_required_mappings_raises() -> None:
    with pytest.raises(
        AttributeError, match="missing required field definitions"
    ):
        _MissingMappingsHandler()


def test_femhandler_contract_key_mismatch_raises() -> None:
    with pytest.raises(
        ValueError, match="Keys of us, eta_us, and us_old must match"
    ):
        _KeyMismatchHandler()


def test_femhandler_contract_valid_definition_passes() -> None:
    handler = _ValidHandler()
    assert set(handler.us.keys()) == {0}
    assert set(handler.vs.keys()) == {0}
