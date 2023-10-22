import pandas as pd
from DataProcess import *
from AccountReuse import *
from HighFrequencyAccess import *
from LoginException import *
from OutOfHoursAccess import *
from UncommonIp import *


if __name__ == '__main__':

    df = DataProcess('../data.csv').process()

    # 1. 业务高频访问
    max_num = 5
    highfrequency = HighFrequencyAccess(max_num)
    # 2. 账户复用
    accountreuse = AccountReuse()
    # 3. 非常用IP
    uncommonip = UncommonIp()
    # 4. 非工作时间
    start = pd.to_datetime('08:00:00').time()
    end = pd.to_datetime('19:00:00').time()
    outHour = OutOfHoursAccess(start, end)
    # 5. 登录异常
    login = LoginException()

    # 异常数据
    ExceptionData = []

    # 测试
    for i, row in df.iterrows():
        # 1. 业务高频访问
        if highfrequency.detection(row):
            ExceptionData.append([row['账号'], row['日期时间'], '业务高频访问'])
        # 2. 账户复用
        if accountreuse.detection(row):
            ExceptionData.append([row['账号'], row['日期时间'], '账号复用'])
        # 3. 非常用IP
        uncommonip.dataload(row)
        # 4. 非工作时间
        if outHour.detection(row):
            ExceptionData.append([row['账号'], row['日期时间'], '非工作时间访问'])
        # 5. 登录异常
        if login.detection(row):
            ExceptionData.append([row['账号'], row['日期时间'], '登录异常'])

    df_ano = uncommonip.detection()
    for i,row in df_ano.iterrows():
        ExceptionData.append([row['异常账号'], row['异常时间'], row['异常类型']])

    for i in range(len(ExceptionData)):
        ExceptionData[i][1] = ExceptionData[i][1].strftime("%Y/%m/%d %H:%M")
    # 保存异常数据为csv
    df_exception = pd.DataFrame(ExceptionData, columns=['异常账号', '异常时间', '异常类型'])
    df_exception = df_exception.sort_values(by='异常时间', ascending=True)
    df_exception.to_csv('../exception.csv', index=False)
