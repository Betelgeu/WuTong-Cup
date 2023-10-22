class AccountReuse:
    def __init__(self) -> None:
        self.account_data = {}
        self.last_interval = None

    # detection()每次检查一条数据, for循环交给外部
    def detection(self, row) -> bool:
        account = row['账号']
        ip = row['源IP']
        timestamp = row['日期时间']

        # 处理新账户
        if account not in self.account_data:
            self.account_data[account] = set()
        # 计算当前时间所在的时间区间
        current_interval = timestamp.floor('2T')  # 将时间戳向下取整到最近的两分钟时间区间
        # 如果是新的时间区间，清空account_data
        if current_interval != self.last_interval and self.last_interval is not None:
           self.account_data = {}
           self.last_interval = current_interval

        self.account_data[account].add(ip)

        if len(self.account_data[account]) >= 3:
            return True
        return False