'''
Time Series Analysis 时间序列分析

'''

from pandas import DataFrame
from numpy import ndarray
import numpy as np
from statsmodels.api import OLS
from statsmodels.api import add_constant
import prettytable as pt
from numpy.linalg import inv
from scipy.stats import f


from .adjust import newey_west_t



class TS_regress() :
    '''
    This class is designed for time series regression, 
        r_{i,t} = \beta_if_t + \epsilon_{i,t}
    to obtain the beta for each asset.
    '''
    def __init__(self, list_y:DataFrame, factor:DataFrame) :
        '''
        This function initializes the object.
        input :
            list_y (list/DataFrame): The return matrix with i rows and t columns.
            factor (ndarray or DataFrame): The factor risk premium return series.
        '''

        if type(list_y).__name__ == 'DataFrame':
            self._name_y = list(list_y.columns)
            self.list_y = [np.array(list_y.iloc[:, i]) for i in range(len(list_y.columns))]
        elif type(list_y).__name__ == 'list':
            self._name_y = None
            self.list_y = list_y
        else:
            raise IOError
        
        if type(factor).__name__ == 'DataFrame':
            self._name_factor = list(factor.columns)
            self.factor = np.array(factor)
        elif type(factor).__name__ == 'ndarray':
            self._name_factor = None
            self.factor = factor
        else:
            raise IOError

    def ts_regress(self, newey_west: bool=True, **kwargs) :
        '''
        This function is for conducting the time series regression.
        input :
            newey_west  (boolean): conduct the newey_west adjustment or not.

        output :
            self.alpha (list): The regression alpha.
            self.e_mat (ndarray): The error matrix.
        
        Example:
        from statsmodels.base.model import Model
        from statsmodels.tools.tools import add_constant
        from EAP.time_series_regress import TS_regress

        X = np.random.normal(loc=0.0, scale=1.0, size=(2000,10))
        y_list = []
        for i in range(10) :
            b = np.random.uniform(low=0.1, high=1.1, size=(10,1))
            e = np.random.normal(loc=0.0, scale=1.0, size=(2000,1))
            y = X.dot(b) + e 
            y_list.append(y)

        re = TS_regress(y_list, X)
        '''

        length = len(self.list_y)
        try :            
            r, c = np.shape(self.factor)
        except:
            r = len(self.factor)
            c = 0
        self.alpha = []
        self.e_mat = np.zeros((r, length))
        self.t_value = np.zeros((length, c+1))
        self.p_value = np.zeros((length, c+1))
        self.params_table = np.zeros((length, c+1))
        self.r_square = np.zeros((length, 1))
        self.adj_r = np.zeros((length, 1))

        for i in range(length) :
            result = OLS(self.list_y[i], add_constant(self.factor)).fit()
            params = result.params
            self.params_table[i, :] = params
            residue = result.resid
            self.alpha.append(params[0])
            self.e_mat[:, i] = residue
            self.r_square[i, :] = result.rsquared
            self.adj_r[i, :] = result.rsquared_adj
            if newey_west == True :
                self.t_value[i, :], self.p_value[i, :] = newey_west_t(self.list_y[i], add_constant(self.factor), params=result.params, constant=False,**kwargs)
            elif newey_west == False:
                self.t_value[i, :], self.p_value[i, :] = result.tvalues, result.pvalues
        
        self.alpha = np.array(self.alpha)

        return self.alpha, self.e_mat

    def fit(self, **kwargs) :
        '''
        Fit model 拟合模型
        '''

        self.ts_regress(**kwargs)
    
    def summary(self) : 
        '''
        Summary 总结
        This function summarize the result, including the GRS test.
        '''

        r, c = np.shape(self.factor)
        length = len(self.list_y)
        table = pt.PrettyTable()
        if self._name_factor is None:
            table.field_names = ['Variable', 'alpha'] + ['factor '+str(i) for i in range(c)]
        else:
            table.field_names = ['Variable', 'alpha'] + self._name_factor
        for i in range(length):
            if self._name_y is None:
                table.add_row([str(i)] + list(np.around(self.params_table[i, :], decimals=4)))
            else:
                table.add_row([self._name_y[i]] + list(np.around(self.params_table[i, :], decimals=4)))
            table.add_row(['t-value'] + list(np.around(self.t_value[i, :], decimals=3)))
            table.add_row(['p-value'] + list(np.around(self.p_value[i, :], decimals=3)))
            table.add_row(['R2'] + list(np.around(self.r_square[i, :], decimals=3)) + ['' for num in range(c)])
            table.add_row(['Adj_R2'] + list(np.around(self.adj_r[i, :], decimals=3)) + ['' for num in range(c)])
              
        print(table)

        grs_stats, grs_p = self.grs()
        print("----------------------------------- GRS Test --------------------------------\n")
        print("GRS Statistics:", np.around(grs_stats[0, 0], decimals=3), "GRS p_value:", np.around(grs_p[0, 0], decimals=3))
        print("-----------------------------------------------------------------------------\n")

    def grs(self) :
        '''
        GRS test GRS检验
        This function conducts the GRS test.
        output :
            grs_stats (list):* The GRS statistics.
            p_value (list):* The p_value.
        '''

        length = len(self.list_y)
        r, c = np.shape(self.factor)
        factor_mean = np.expand_dims(np.mean(self.factor, axis=0), axis=0)
        
        temp_factor = self.factor - factor_mean
        sigma_factor_mat = 1 / r * temp_factor.T.dot(temp_factor)
        error_mat = 1 / r * self.e_mat.T.dot(self.e_mat)

        grs_stats = (r - length - c) / (length * (1 + factor_mean.dot(inv(sigma_factor_mat)).dot(factor_mean.T)))\
                    * self.alpha.dot(inv(error_mat)).dot(self.alpha.T)
        p_value = 1 - f.cdf(grs_stats, length, r-length-c)

        return grs_stats, p_value
