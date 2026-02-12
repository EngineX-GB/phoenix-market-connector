from abc import ABC

from src.model.PropertyManager import PropertyManager


class PhoenixAbstractOrderLoader(ABC):

    def cancel_order(self, order_ref: str):
        pass

    def amend_order(self, order_ref: str):
        pass

    def execute_order(self):
        pass

    def raise_order(self):
        pass

    def show_orders(self):
        pass

