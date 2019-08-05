from pypfopt.efficient_frontier import EfficientFrontier
import pypfopt.expected_returns as expected_returns
import pypfopt.risk_models as risk_models
import pandas as pd
import os
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path", action='store',type=str,default='E:\\CODE/python/Deecamp/Proj/Data/funds/nav/')
    parser.add_argument("-s","--subdirs",action='store',type=str,default="00")
    parser.add_argument("-v","--volatility",action='store',type=float,default=-1)
    parser.add_argument("-r","--risk_free_rate",action='store',type=float,default=0.02)
    args=parser.parse_args()

    nav_path = args.path
    # 'E:\\CODE/python/Deecamp/Proj/Data/funds/nav/'
    #"C:/Users/qin_t/Desktop/PortfolioOptimization/funds/funds/nav"
    dateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d")
    data_list = []

    for subdir in (os.listdir(nav_path) if args.subdirs=="all" else args.subdirs.split(',')):
        print(subdir)
        if not os.path.isdir(nav_path + "/" + subdir):
            continue
        for filename in os.listdir(nav_path + "/" + subdir):
            filepath = nav_path + "/" + subdir + "/" + filename
            tdata = pd.read_csv(str(filepath),
                                parse_dates=['datetime'],
                                index_col='datetime',
                                date_parser=dateparser  # 按时间对齐
                                )
            if 'unit_net_value' in tdata.columns: # 非日结
                data_list.append(
                    tdata[['unit_net_value']]
                        .rename(columns={'unit_net_value': filename[0:6]}, index=str).astype('float'))
            else: # 日结
                data_list.append(
                    (tdata[['weekly_yield']]+1)
                        .rename(columns={'weekly_yield': filename[0:6]}, index=str).astype('float'))

    data = pd.concat(data_list, axis=1)

    print(data.head())


    # efficient frontier
    mu=expected_returns.ema_historical_return(data)
    S=risk_models.CovarianceShrinkage(data).ledoit_wolf()
    ef=EfficientFrontier(mu,S)

    if args.volatility<0:
        print(ef.max_sharpe(args.risk_free_rate))
    else:
        print(ef.efficient_risk(args.volatility,args.risk_free_rate))

    ef.portfolio_performance(True)
