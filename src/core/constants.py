# Risk Parameters
MAX_RISK_PER_TRADE_PCT = 0.01  # 1% of total capital per trade
MAX_DAILY_LOSS_PCT = 0.02      # 2% of total capital daily loss limit
MAX_WEEKLY_LOSS_PCT = 0.05     # 5% of total capital weekly loss limit
MAX_MONTHLY_LOSS_PCT = 0.10    # 10% of total capital monthly loss limit
MAX_OPEN_POSITIONS = 5         # Maximum number of concurrent positions

# Stop Loss / Trailing Stop
ATR_STOP_LOSS_MULT = 2.0       # Stop loss distance in ATR multiples
TRAILING_STOP_ACTIVATION = 1.5 # Trailing stop activates when price moves this many ATRs in favor
TRAILING_STOP_DIST = 1.0       # Distance for trailing stop in ATR multiples

# Filters and Thresholds
VIX_WARNING_THRESHOLD = 25     # Reduce position size above this VIX
VIX_HALT_THRESHOLD = 35        # Halt trading above this VIX
MIN_AGENT_CONSENSUS_PCT = 0.60 # Minimum % of agents needed to agree on direction
MIN_CONFIDENCE_SCORE = 70.0    # Minimum confidence score out of 100

# API Limits
MAX_ORDERS_PER_SECOND = 10     # SEBI limit for retail API trading
