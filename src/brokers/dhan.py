import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.brokers.base import BaseBroker
import logging
from dhanhq import dhanhq
from dotenv import load_dotenv
import pandas as pd

logger = logging.getLogger(__name__)

SYMBOL_MAPPING = {
    "RELIANCE.NS": "2885",
    "HDFCBANK.NS": "1333",
    "TCS.NS": "11536",
    "INFY.NS": "1594",
    "SBIN.NS": "3045"
}

class DhanBroker(BaseBroker):
    """DhanHQ Sandbox implementation for paper trading"""
    
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("DHAN_CLIENT_ID", "")
        self.access_token = os.getenv("DHAN_ACCESS_TOKEN", "")
        self.dry_run = os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes")
        self.dhan = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """Establish connection with the DhanHQ Sandbox"""
        logger.info("Connecting to Dhan Sandbox...")
        
        if self.dry_run:
            logger.info("DRY_RUN is enabled. Bypassing actual Dhan connection.")
            self.is_connected = True
            return True
            
        try:
            if not self.client_id or not self.access_token:
                logger.error("Dhan credentials not found in environment variables.")
                return False
                
            self.dhan = dhanhq(self.client_id, self.access_token)
            # Make a test call to verify connection
            funds = self.dhan.get_fund_limits()
            if funds:
                self.is_connected = True
                logger.info("Successfully connected to Dhan Sandbox.")
                return True
            else:
                logger.warning("Connection check failed: No funds data returned.")
                return False
        except Exception as e:
            logger.error(f"Failed to connect to Dhan Sandbox: {str(e)}")
            return False
            
    def get_ltp(self, symbol: str) -> float:
        """Get Last Traded Price for a symbol. 
        Note: Dhan API requires exchange_segment and security_id. 
        For simplicity, assuming NSE EQ.
        """
        if not self.is_connected:
            return 0.0
        
        if self.dry_run:
            logger.info(f"[DRY RUN] get_ltp called for {symbol}")
            return 0.0
            
        security_id = SYMBOL_MAPPING.get(symbol)
        if not security_id:
            logger.error(f"No security mapping found for symbol: {symbol}")
            return 0.0
            
        logger.warning("get_ltp via DhanHQ API not fully implemented. Please use yfinance.")
        return 0.0
        
    def get_historical_data(self, symbol: str, start_date: datetime, end_date: datetime, interval: str) -> List[Dict[str, Any]]:
        """Get historical OHLCV data."""
        if self.dry_run:
            logger.info(f"[DRY RUN] get_historical_data called for {symbol}")
            return []
            
        logger.warning("get_historical_data via DhanHQ API not fully implemented. Please use yfinance.")
        return []
        
    def place_order(self, symbol: str, action: str, quantity: int, price: float, order_type: str = "LIMIT") -> str:
        """Place an order and return order ID"""
        if not self.is_connected:
            return ""
            
        if self.dry_run:
            order_id = f"DRY_RUN_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            logger.info(f"[DRY RUN] Would place {action} order for {quantity} {symbol} at {price}. OrderID: {order_id}")
            return order_id
            
        try:
            # Map action to Dhan API constants
            transaction_type = self.dhan.BUY if action.upper() == "BUY" else self.dhan.SELL
            o_type = self.dhan.LIMIT if order_type.upper() == "LIMIT" else self.dhan.MARKET
            
            security_id = SYMBOL_MAPPING.get(symbol)
            if not security_id:
                logger.error(f"Cannot place order: No security mapping found for symbol: {symbol}")
                return ""
            
            res = self.dhan.place_order(
                security_id=security_id,
                exchange_segment=self.dhan.NSE,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=o_type,
                product_type=self.dhan.INTRA,
                price=price
            )
            
            if res.get("status") == "success":
                order_id = res.get("data", {}).get("orderId", "")
                logger.info(f"Order placed successfully: {order_id}")
                return order_id
            else:
                logger.error(f"Failed to place order: {res}")
                return ""
        except Exception as e:
            logger.error(f"Exception during place_order: {str(e)}")
            return ""
            
    def modify_order(self, order_id: str, new_quantity: Optional[int] = None, new_price: Optional[float] = None) -> bool:
        """Modify an existing order"""
        if not self.is_connected:
            return False
        
        try:
            res = self.dhan.modify_order(
                order_id=order_id,
                order_type=self.dhan.LIMIT if new_price else self.dhan.MARKET,
                leg_name="NA",
                quantity=new_quantity,
                price=new_price or 0.0,
                validity=self.dhan.DAY
            )
            return res.get("status") == "success"
        except Exception as e:
            logger.error(f"Exception during modify_order: {str(e)}")
            return False
            
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order"""
        if not self.is_connected:
            return False
            
        try:
            res = self.dhan.cancel_order(order_id=order_id)
            return res.get("status") == "success"
        except Exception as e:
            logger.error(f"Exception during cancel_order: {str(e)}")
            return False
            
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions"""
        if not self.is_connected:
            return []
            
        try:
            res = self.dhan.get_positions()
            if res.get("status") == "success":
                return res.get("data", [])
            return []
        except Exception as e:
            logger.error(f"Exception during get_positions: {str(e)}")
            return []
