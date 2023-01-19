from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class SellEvent(Base):
    """sell Event"""

    __tablename__ = "sell_event"

    id = Column(Integer, primary_key=True)
    sell_id = Column(String(250), nullable=False)
    item_name = Column(String(250), nullable=False)
    item_price = Column(Float(24), nullable=False)
    sell_qty = Column(Integer, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, sell_id, item_name, item_price, sell_qty, trace_id):
        """Initializes a sell Event"""
        self.sell_id = sell_id
        self.item_name = item_name
        self.item_price = item_price
        self.sell_qty = sell_qty
        self.trace_id = trace_id

    def to_dict(self):
        """Dictionary Representation of a sell Event"""
        dict = {}
        dict["id"] = self.id
        dict["sell_id"] = self.sell_id
        dict["item_name"] = self.item_name
        dict["item_price"] = self.item_price
        dict["sell_qty"] = self.sell_qty
        dict["trace_id"] = self.trace_id

        return dict
