INIT_STAGE = "InitStage"
EXTENDED_STAGE = "ExtendedStage"
STAGE_CONFIGS = {
    INIT_STAGE:([i for i in range(700, 901, 100)], range(3)),
    EXTENDED_STAGE:([i for i in range(100, 2001, 100)], range(5))}
TX_MAX_DURATIONS = range(100, 501, 100)
RETRIES = range(5)
MAX_RX_TX_PERIOD_SECS = 0.255
DEFAULT_BRG_ID = "FFFFFFFFFFFF"