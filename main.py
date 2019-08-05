from Data_solve import *
from Data_Read import *
from MyCrawyer import *

if __name__ == '__main__':
    # 获取公司列表
    url_company = 'http://fund.eastmoney.com/js/jjjz_gs.js?dt=1463791574015'
    get_company_list(url_company)
    # 获取基金列表
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    get_fund_list(url)
    # 基金信息下载与处理
    get_pingzhong_data()
    # std 和夏普比率信息下载
    download_f10_ts_data()
    # 基金经理信息下载
    download_manager_info()


    # std 和夏普比率信息处理
    solve_f10_data()
    # 基金经理信息处理
    solve_manager_info()
    # pingzhong data 处理
    solve_crawler3()
