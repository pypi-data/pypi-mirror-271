"""Contains methods for accessing the API"""

from typing import Type

from .congress import CongressEndpoints
from .contract import ContractEndpoints
from .darkpool import DarkpoolEndpoints
from .earnings import EarningsEndpoints
from .etfs import EtfsEndpoints
from .flow import FlowEndpoints
from .market import MarketEndpoints
from .screener import ScreenerEndpoints
from .seasonality import SeasonalityEndpoints
from .stock import StockEndpoints


class UnusualWhalesApiClientApi:
    @classmethod
    def congress(cls) -> Type[CongressEndpoints]:
        return CongressEndpoints

    @classmethod
    def darkpool(cls) -> Type[DarkpoolEndpoints]:
        return DarkpoolEndpoints

    @classmethod
    def earnings(cls) -> Type[EarningsEndpoints]:
        return EarningsEndpoints

    @classmethod
    def etfs(cls) -> Type[EtfsEndpoints]:
        return EtfsEndpoints

    @classmethod
    def market(cls) -> Type[MarketEndpoints]:
        return MarketEndpoints

    @classmethod
    def flow(cls) -> Type[FlowEndpoints]:
        return FlowEndpoints

    @classmethod
    def contract(cls) -> Type[ContractEndpoints]:
        return ContractEndpoints

    @classmethod
    def screener(cls) -> Type[ScreenerEndpoints]:
        return ScreenerEndpoints

    @classmethod
    def seasonality(cls) -> Type[SeasonalityEndpoints]:
        return SeasonalityEndpoints

    @classmethod
    def stock(cls) -> Type[StockEndpoints]:
        return StockEndpoints
