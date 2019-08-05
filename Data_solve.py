import pandas as pd
from datetime import datetime
from Data_Read import *
import re

def data_select():
    benchmark_time = datetime.strptime('2015-05-04','%Y-%m-%d')
    listed_to_delisted = []     # 上市持续时间
    establishment_to_stop = []  # 建立持续时间
    TabuList = []               # 筛选出局的股票代码
    data = pd.read_csv('E:\\CODE\Python\Deecamp\Proj\Data\instruments_ansi.csv',encoding='ANSI')
    for i in range(0,len(data['establishment_date'])):
        d1 = datetime.strptime(data['establishment_date'][i], '%Y-%m-%d')
        d3 = datetime.strptime(data['listed_date'][i], '%Y-%m-%d')
        if data['stop_date'][i] == '0000-00-00':
            establishment_to_stop.append(0)
            listed_to_delisted.append(0)
        else:
            d2 = datetime.strptime(data['stop_date'][i], '%Y-%m-%d')
            d4 = datetime.strptime(data['de_listed_date'][i], '%Y-%m-%d')
            delta1 = d2 - d1
            delta2 = d4 - d3
            establishment_to_stop.append(delta1.days)
            listed_to_delisted.append(delta2.days)
            # 与基准时间比较
            if (d2 - benchmark_time).days < 0:
                TabuList.append(data['code'][i])

    data['listed_to_delisted'] = listed_to_delisted
    data['establishment_to_stop'] = establishment_to_stop
    data.to_csv('Data/new.csv',encoding='ANSI')


def solve_fund_info():
    rootDir = 'E:\\CODE/python/Deecamp/Proj/Data/fundInfo/'
    org_data_list = data_read(rootDir)
    data_list = {}
    data_list = {'fS_name':[],
                'fS_code':[],
                'fund_sourceRate':[]
                ,'fund_Rate':[]
                ,'fund_minsg':[]
                ,'syl_1n':[]
                ,'syl_6y':[]
                ,'syl_3y':[]
                ,'syl_1y':[]
                ,'Data_holderStructure':[]
                ,'Data_assetAllocation':[]
                ,'Data_currentFundManager':[]
                ,'Data_buySedemption':[]}
    for i in range(0,len(org_data_list)):
        strs = re.findall(r'var(.*?);',org_data_list[i])
        fund_info = {}
        for j in range(0,len(strs)):
            tmp = strs[j].split('=')
            var_name = tmp[0].strip()
            fund_info[var_name] = [tmp[1]]
        for key in data_list.keys():
            if key in fund_info.keys() :
                if key is 'Data_assetAllocation' and 'Data_assetAllocationCurrency' in fund_info.keys():
                    data_list[key].append(fund_info['Data_assetAllocationCurrency'])
                    data_list['Data_buySedemption'].append(fund_info[key])
                elif 'Data' not in key and key != 'zqCodes':
                    data_list[key].append(eval(fund_info[key][0]))
                else:
                    data_list[key].append(fund_info[key][0])
            # elif len(data_list[key])<=i:
            #     data_list[key].append('')
    df = pd.DataFrame(data_list)
    df.to_csv('Data/crawler3.csv',encoding='ANSI')



def solve_f10_data():
    rootDir = 'E:\\CODE/python/Deecamp/Proj/Data/f10_ts/'
    org_data_list = data_read(rootDir)
    data_list = {}
    data_list['基金号'] = []
    data_list['近1年std']=[]
    data_list['近2年std']=[]
    data_list['近3年std']=[]
    data_list['近1年夏普率'] = []
    data_list['近2年夏普率'] = []
    data_list['近3年夏普率'] = []

    for i in range(0,len(org_data_list)):
        a = re.findall(r'<td class=\'num\'>(.*?)</td>',org_data_list[i])
        if len(a)>0:
            data_list['近1年std'].append(a[0])
            data_list['近2年std'].append(a[1])
            data_list['近3年std'].append(a[2])
            data_list['近1年夏普率'].append(a[3])
            data_list['近2年夏普率'].append(a[4])
            data_list['近3年夏普率'].append(a[5])
            a = re.findall(r'tsdata_(.*?).htm',org_data_list[i])
            code  = '%06d' %int(a[0])
            data_list['基金号'].append(code)
    df = pd.DataFrame(data_list,index=data_list['基金号'])
    df.to_csv('Data/f10_ts/std and sharp ratio.csv',encoding='ANSI')


def solve_crawler3():
    df = pd.read_csv('Data/crwaler3.csv',encoding='ANSI')
    data_list = {}
    # 经理信息
    data_list['基金经理'] = []
    data_list['经理工作时间'] = []
    data_list['经理管理基金size'] = []
    # 占净比
    data_list['股票占净比'] = []
    data_list['债券占净比'] = []
    data_list['现金占净比'] = []
    data_list['净资产'] = []
    data_list['categories1']=[]
    # 买卖信息
    data_list['期间申购'] = []
    data_list['期间赎回'] = []
    data_list['总份额']=[]
    data_list['categories2']=[]
    # 比例信息
    data_list['机构持有比例']=[]
    data_list['个人持有比例']=[]
    data_list['内部持有比例']=[]
    data_list['categories3']=[]
    # 占净比信息
    tmp = df['Data_assetAllocation']
    for i in range(0,len(tmp)):
        strs = re.findall(r'\"data\":(.*?),\"',tmp[i])
        t = re.findall(r'\"categories\":(.*?)}',tmp[i])
        if len(strs)==4:
            data_list['股票占净比'].append(strs[0])
            data_list['债券占净比'].append(strs[1])
            data_list['现金占净比'].append(strs[2])
            data_list['净资产'].append(strs[3])
        else:
            strs = re.findall(r'\"data\":(.*?)\}',tmp[i])
            data_list['股票占净比'].append(strs[0])
            data_list['债券占净比'].append(strs[1])
            data_list['现金占净比'].append(strs[2])
            data_list['净资产'].append('')
            t = t[0].split(',"series":')
        if len(t)>0:
            data_list['categories1'].append(t[0])
        else:
            data_list['categories1'].append('')
    del df['Data_assetAllocation']

    # 买卖信息
    tmp = df['Data_buySedemption']
    for i in range(0,len(tmp)):
        strs = re.findall(r'\"data\":(.*?)}',tmp[0])
        t = re.findall(r'\"categories\":(.*?)}',tmp[i])
        if len(strs)>0:
            data_list['期间申购'].append(strs[0])
            data_list['期间赎回'].append(strs[1])
            data_list['总份额'].append(strs[2])
        else:
            data_list['期间申购'].append('')
            data_list['期间赎回'].append('')
            data_list['总份额'].append('')
        if len(t)>0:
            data_list['categories2'].append(t[0])
        else:
            data_list['categories2'].append('')
    del df['Data_buySedemption']

    # 经理信息
    tmp = df['Data_currentFundManager']
    for i in range(0,len(tmp)):
        name = re.findall(r'\"name\":(.*?),',tmp[i])
        workTime = re.findall(r'\"workTime\":(.*?),',tmp[i])
        fundSize = re.findall(r'\"fundSize\":(.*?),',tmp[i])
        if len(workTime)>0:
            data_list['经理工作时间'].append(eval(workTime[0]))
        else:
            data_list['经理工作时间'].append('')
        if len(name) > 0:
            data_list['基金经理'].append(name[0])
        else:
            data_list['基金经理'].append('')
        if len(fundSize) > 0:
            data_list['经理管理基金size'].append(eval(fundSize[0]))
        else:
            data_list['经理管理基金size'].append('')
    del df['Data_currentFundManager']

    # 比例信息
    tmp = df['Data_holderStructure']
    for i in range(0,len(tmp)):
        strs = re.findall(r'\"data\":(.*?)\}',tmp[i])
        t = re.findall(r'\"categories\":(.*?)}',tmp[i])
        if len(strs)>0:
            data_list['机构持有比例'].append(strs[0])
            data_list['个人持有比例'].append(strs[1])
            data_list['内部持有比例'].append(strs[2])
        else:
            data_list['机构持有比例'].append('')
            data_list['个人持有比例'].append('')
            data_list['内部持有比例'].append('')
        if len(t)>0:
            data_list['categories3'].append(t[0])
        else:
            data_list['categories3'].append('')
    del df['Data_holderStructure']
    df2 = pd.DataFrame(data_list)
    df = pd.concat([df,df2],axis=1)
    df.to_csv('Data/data.csv',encoding = 'ANSI')


def solve_manager_info():
    rootDir = 'E:\\CODE/python/Deecamp/Proj/Data/managerInfo/'
    org_data_list = data_read(rootDir)
    name_list = []
    manager_info_list={'name':[],'code':[]}
    for i in range(0, len(org_data_list)):
        data_list = {'姓名':[], '上任日期':[],'经理代号':[],'简介':[], '基金名称':[],'基金代码':[],'基金类型':[],'起始时间':[],'截止时间':[],'任职天数':[],'任职回报':[],'同类平均':[],'同类排名':[]}
        # 姓名
        a = re.findall(r'姓名(.*?)<div class="space10"></div>', org_data_list[i])
        for ii in range(0,len(a)):
            b = a[ii]
            name = re.findall(r'\">(.*?)</a></p><p><strong>', b)[0]
            if name not in name_list:
                name_list.append(name)
                duty_date = re.findall(r'上任日期：</strong>(.*?)</p>', b)[0]
                brief_intro = re.findall(r'</p><p>(.*?)</p><p class="tor">', b)[0].split('<p>')[-1]
                manager_code = re.findall(r'"http://fund.eastmoney.com/manager/(.*?).html',b)[0]
                data_list['姓名'].append(name)
                data_list['上任日期'].append(duty_date)
                data_list['经理代号'].append(manager_code)
                data_list['简介'].append(brief_intro)
                fund_info_list = re.findall(r'html\"(.*?)</tr>', b)[1:]

                # manager list
                manager_info_list['name'].append(name)
                manager_info_list['code'].append(manager_code)

                for iii in range(0, len(fund_info_list)):
                    fund_list = re.findall(r'>(.*?)</td>' or r'>(.*?)</a></td>',fund_info_list[iii])
                    fund_list[0] = fund_list[0].split('<')[0]
                    fund_list[1] = re.findall(r'>(.*?)<', fund_list[1])[0]
                    data_list['基金名称'].append(fund_list[1])
                    data_list['基金代码'].append(fund_list[0])
                    data_list['基金类型'].append(fund_list[2])
                    data_list['起始时间'].append(fund_list[3])
                    data_list['截止时间'].append(fund_list[4])
                    data_list['任职天数'].append(fund_list[5])
                    data_list['任职回报'].append(fund_list[6])
                    data_list['同类平均'] .append(fund_list[7])
                    data_list['同类排名'] .append(fund_list[8])
                    if iii>0:
                        data_list['姓名'].append('')
                        data_list['上任日期'].append('')
                        data_list['经理代号'].append('')
                        data_list['简介'].append('')
                dir = 'Data/managerSlv/'+name+'.csv'
                df = pd.DataFrame(data_list)
                order = ['姓名','上任日期','经理代号','简介','基金名称','基金代码','基金类型','起始时间','截止时间','任职天数','任职回报','同类平均','同类排名']
                df = df[order]
                df.to_csv(dir,encoding='ANSI')
    df_manager_info_list = pd.DataFrame(manager_info_list)
    df_manager_info_list.to_csv('Data/manager.csv',encoding='ANSI')


if __name__ == '__main__':
    solve_manager_info()
