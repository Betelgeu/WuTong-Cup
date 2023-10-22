from datetime import timedelta

class HighFrequencyAccess:

    class User:
        __slots__ = ('time', 'business')
        def __init__(self,timestamp):
            self.time=timestamp
            self.business={}

    def __init__(self, max_num) -> None:
        self.max_num = max_num
        self.user_dict = {}

    def detection(self,row) -> bool:
        user_id= row['账号']
        timestamp = row['日期时间']
        transaction  = row['操作内容']
        if user_id in self.user_dict:
            user = self.user_dict[user_id]
            if timestamp-user.time >= timedelta(minutes=1) or timestamp.minute!=user.time.minute:
                del self.user_dict[user_id]
                # 删除之前的数据
                self.user_dict[user_id] = HighFrequencyAccess.User(timestamp)

            user = self.user_dict[user_id]
        else:
            user = HighFrequencyAccess.User(timestamp)
        user.business[transaction] = user.business.get(transaction, 0) + 1
        self.user_dict[user_id] = user
        
        if user.business[transaction]>self.max_num:
            return True
        else:
            return False