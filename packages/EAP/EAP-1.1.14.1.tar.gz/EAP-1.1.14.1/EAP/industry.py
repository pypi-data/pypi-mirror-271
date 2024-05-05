'''
Factor model for industry 商用因子模型
'''

import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

from .portfolio_analysis import Univariate

class Portfolio(Univariate):
    '''
    construct portfolio and backtest 
    '''
    def __init__(self, sample):
        super().__init__(sample)


    def divide_token(self):
        stocklist = dict()
        group_time = super().divide_by_time(self.sample)
        self._average_group_by_time = super().average_by_time()
        self._average = self._average_group_by_time.mean(axis=1)

        for t_time in range(len(group_time)):
            group = group_time[t_time]
            if self._weight == False:
                token = group[:, 3]
            elif self._weight == True:
                token = group[:, 4]
            else:
                return IOError
    
            label = self._label[t_time]

            stocklist_eachtime = dict()

            for n_group in range(self.number+1):
                location = np.where(label==n_group)
                stocklist_eachtime[n_group] = token[location]            
            
            stocklist[self._time[t_time]] = stocklist_eachtime


        self.stocklist = stocklist
        return stocklist
    
    def extract_portfolio(self, group_num):
        '''
        extract portfolio return series
        '''
        return self._average_group_by_time[group_num, :]
    
    def plot(self, group_num):
        '''
        plot portfolio return
        '''
        ax = plt.plot(self._time, self._average_group_by_time[group_num, :], label='Group'+str(group_num+1))
        return ax
    
    def plot_all(self):
        '''
        plot all portfolio return
        '''
        for i in range(self.number+1):
            self.plot(i)
        
        plt.title('Portfolio Return')
        plt.legend()

    def group_turnover(self, group_num):
        '''
        calculate group turnover
        '''
        turnover_each_time = np.zeros(len(self._time) - 1)
        stocklist_previous = self.stocklist[self._time[0]][group_num]

        for t_time in range(len(self._time)-1):
            stocklist_eachtime = self.stocklist[self._time[t_time + 1]][group_num]
            stocklist_common = set(stocklist_eachtime) & set(stocklist_previous)
            turnover_each_time[t_time] = 1 - len(stocklist_common) / len(stocklist_eachtime)

            # upgrade stock_previous
            stocklist_previous = stocklist_eachtime
        
        return turnover_each_time

    def turnover(self):
        '''
        calculate all turnover : 计算全组换手率
        '''
        turnover_allgroup = np.zeros((self.number+1, len(self._time)-1))
        for num in range(self.number + 1):
            turnover_allgroup[num, :] = self.group_turnover(num)
        
        self._turnover_allgroup = turnover_allgroup
        
        return turnover_allgroup

    def compound_return(self):
        '''
        compound return : 累计收益率
        '''
        average_group_by_time_add_one = np.c_[np.zeros((self.number+1, 1)), self._average_group_by_time]
        self._group_compound_return = np.cumprod(1 + average_group_by_time_add_one, axis=1)

        return self._group_compound_return
    
    def plot_compound_return(self):
        '''
        plot compound return
        '''
        for group_num in range(self.number+1):
            plt.plot(np.r_[self._time[0], self._time], self._group_compound_return[group_num, :], label='Group'+str(group_num+1))

        plt.title('Compound Return')        
        plt.legend()

    def drawdown(self, group_num):
        '''
        calculate drawdown : 计算回撤
        '''
        group_compound_return = self.compound_return()[group_num, :]
        group_max = group_compound_return[0]
        temp_drawdown = 0.0
        group_drawdown = np.zeros((len(group_compound_return), 1))

        for t_time in range(len(group_compound_return)):
            if group_compound_return[t_time] < group_max:
                group_drawdown[t_time] = (group_compound_return[t_time] - group_max) / group_max
            else:
                group_drawdown[t_time] = 0.0
                group_max = group_compound_return[t_time]

            temp_drawdown = group_drawdown[t_time]

        return group_drawdown

    def maxdrawdown(self):
        '''
        calculate MAX drawdown : 计算最大回撤
        '''
        all_drawndown = np.zeros(np.shape(self._group_compound_return))

        for num in range(self.number+1):
            all_drawndown[num, :] = self.drawdown(num)[:, 0]
        
        self._all_drawdown = all_drawndown
        self._max_drawdown = self._all_drawdown.min(axis=1)

        return self._max_drawdown        
    
    def plot_drawdown(self):
        '''
        plot drawdown : 画出回撤
        '''
        for group_num in range(self.number+1):
            plt.plot(np.r_[self._time[0], self._time], self._all_drawdown[group_num, :], label='Group'+str(group_num+1))
        
        plt.plot('Max DrawDown')
        plt.legend()

    def sharpe_ratio(self):
        '''
        calculate sharp ratio
        '''
        self._group_sharpe_ratio = self._average_group_by_time.mean(axis=1) / self._average_group_by_time.std(axis=1)
        
        return self._group_sharpe_ratio
    
    def backtest(self):
        '''
        Backtest : 回测
        '''
        
        self.divide_token()
        self.compound_return()
        self.turnover()
        self.maxdrawdown()
        self.sharpe_ratio()

    def backtest_summary(self, decimals=3):
        '''
        Backtest summary : 回测结果
        '''
        backtest_table = PrettyTable(["Statistics", "Value"])
        
        for group in range(self.number+1):
            backtest_table.add_row(["Group  "+str(group+1), " "])
            backtest_table.add_row(["Average return", np.around(self._average[group], decimals=decimals)])
            backtest_table.add_row(["compounded return", np.around(self._group_compound_return[group, -1], decimals=decimals)])
            backtest_table.add_row(["Turnover", np.around(self._turnover_allgroup.mean(axis=1)[group], decimals=decimals)])
            backtest_table.add_row(["MaxDrawdown", np.around(self._max_drawdown[group], decimals=decimals)])
            backtest_table.add_row(["Sharpte Ratio", np.around(self._group_sharpe_ratio[group], decimals=decimals)])

            if group != self.number:
                backtest_table.add_row(["   ", "   "])

        print(backtest_table)
