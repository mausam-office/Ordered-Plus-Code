ROWS = list(map(lambda x: str(x), range(9, 2, -1)))
COLUMNS = list(map(lambda x: str(x), list(range(2, 10)) + list("CFGHJMPQRV")))

LEVEL2_COLUMNS = list(map(lambda x: str(x), list(range(2, 10)) + list("CFGHJMPQRVWX")))
LEVEL2_ROWS = LEVEL2_COLUMNS[::-1]
