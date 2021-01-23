from app.models.trade_type import TradeType
from app.schemas.trade_type import TradeTypeCreate, TradeTypeUpdate
from app.crud.base import CRUDBase


class CRUDTradeType(CRUDBase[TradeType, TradeTypeCreate, TradeTypeUpdate]):
    pass


trade_type = CRUDTradeType(TradeType)