from datetime import timedelta


class LoginException:
    class User:
        __slots__ = ('time', 'cnt','ips')
        def __init__(self,timestamp):
            self.time=timestamp
            self.cnt=0
            self.ips=set()
    def __init__(self) -> None:
        self.user_dict = {}

    def detection(self,row) -> int:
        user_id= row['账号']
        user_ip = row['源IP']
        timestamp = row['日期时间']
        
        if user_id in self.user_dict:
            user = self.user_dict[user_id]
            if timestamp-user.time >= timedelta(minutes=1) or timestamp.minute!=user.time.minute:
                del self.user_dict[user_id]
                # 删除之前的数据
                user = self.User(timestamp)
        else:
            user = self.User(timestamp)
        user.cnt+=1
        user.ips.add(user_ip)
        self.user_dict[user_id] = user
        if user.cnt>=8 or len(user.ips)>=2:
            return True
        else:
            return False