class OutOfHoursAccess:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def detection(self, row) -> bool:
        datetime_value = row['日期时间'].time()
        # TODO: 19:00:00算不算？
        if not (self.start <= datetime_value < self.end):
            # print(f"Row {row}: {datetime_value} is not in the range.")
            return True
        return False
