from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

class BaseBroker(ABC):
    """Abstract base class for all broker implementations"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection with the broker"""
        pass
        
    @abstractmethod
    def get_ltp(self, symbol: str) -> float:
        """Get Last Traded Price for a symbol"""
        pass
        
    @abstractmethod
    def get_historical_data(self, symbol: str, start_date: datetime, end_date: datetime, interval: str) -> List[Dict[str, Any]]:
        """Get historical OHLCV data"""
        pass
        
    @abstractmethod
    def place_order(self, symbol: str, action: str, quantity: int, price: float, order_type: str = "LIMIT") -> str:
        """Place an order and return order ID"""
        pass
        
    @abstractmethod
    def modify_order(self, order_id: str, new_quantity: Optional[int] = None, new_price: Optional[float] = None) -> bool:
        """Modify an existing order"""
        pass
        
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order"""
        pass
        
    @abstractmethod
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions"""
        pass
