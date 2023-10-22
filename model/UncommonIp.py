import pandas as pd


class UncommonIp:

    class IpData:
        __slots__ = ('count', 'time')
        def __init__(self) -> None:
            self.count = 0
            self.time = []

    def __init__(self):
        self.account_data = {}

    def dataload(self, row):
        account = row['账号']
        ip = row['源IP']
        timestamp = row['日期时间']
        # 如果字典里没有这个用户，初始化
        if account not in self.account_data:
            self.account_data[account] = {'total':0, 'ips':{}}
        
        self.account_data[account]['total'] += 1
        # 如果用户的ips里没有这个ip，初始化\n",
        if ip not in self.account_data[account]['ips']:
            self.account_data[account]['ips'][ip] = UncommonIp.IpData()
        
        self.account_data[account]['ips'][ip].count += 1
        # 如果超过count已经超过4就不再统计ip地址了\n",
        if self.account_data[account]['ips'][ip].count <= 4:
            self.account_data[account]['ips'][ip].time.append(timestamp)


    def detection(self):
        user_list = []
        time_list = []
        for account, user_data in self.account_data.items():
            if user_data['total'] >= 100:
                for _, ip_data in user_data['ips'].items():
                    if ip_data.count < 5:
                        user_id = account
                        for time in ip_data.time:
                            user_list.append(user_id)
                            time_list.append(time)
        data = {
            '异常账号': user_list,
            '异常时间': time_list,
            '异常类型': ['非常用IP访问'] * len(user_list)
        }
        df_ano = pd.DataFrame(data)
        
        return df_ano
