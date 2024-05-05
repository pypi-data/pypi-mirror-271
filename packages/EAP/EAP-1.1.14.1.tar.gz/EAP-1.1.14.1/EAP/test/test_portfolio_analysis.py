# %% Set system path
import sys,os

from numpy import average

sys.path.append(os.path.abspath(".."))

#%% test class ptf_analysis()
def test_ptf_analysis() :
    '''
    TEST ptf_analysis
    contruct samples:
        1. generate character 构建分类特征
        2. generate breakpoint given the character 给定特征生成间断点
        3. generate the future sample return 生成未来样本收益/数值
    '''
     
    from portfolio_analysis import ptf_analysis as ptfa
    import matplotlib.pyplot as plt
    
    import numpy as np
    
    # generate character
    character = np.random.normal(0,100,10000)
    # generate breakpoint
    breakpoint = ptfa().select_breakpoints(character=character, number=9)
    print('Generated breakpoint:', breakpoint)
    # compare with the true breakpoint
    for i in np.linspace(0, 100, 11):
        print('True breakpoint', i, '%:', np.percentile(character,i))
    
    # generate the groups     
    print('The Label of unique value:\n', np.sort(np.unique(ptfa().distribute(character, breakpoint))))
    # plot the histogram of the label 
    # each group have the same number of samples
    plt.hist(ptfa().distribute(character, breakpoint))
    label = ptfa().distribute(character, breakpoint)[:, 0]
    # print the label
    # print('Label:\n', ptfa().distribute(character, breakpoint))
    
    # generate the future sample return
    sample_return = character/100 + np.random.normal()
    ave_ret = ptfa().average(sample_return, label)
    # print the groups return
    print('average return for groups:\n', ave_ret)

    # test function average for Bivariate
    character_1 = np.random.normal(0, 100, 10000)
    character_2 = np.random.normal(0, 100, 10000)
    # generate breakpoint
    breakpoint_1 = ptfa().select_breakpoints(character=character_1, number=9)
    breakpoint_2 = ptfa().select_breakpoints(character=character_2, number=9)
    # attach the label
    label_1 = ptfa().distribute(character_1, breakpoint_1)[:, 0]
    label_2 = ptfa().distribute(character_2, breakpoint_2)[:, 0]
    
    label = [label_1, label_2]
    print(label_1,'\n', label_2)
    # generate the future sample return
    sample_return = character_1/100 - character_2/100 + np.random.normal()
    ave_ret = ptfa().average(sample_return, label, cond='bi')
    print(ave_ret)

    # generate time 
    year=np.ones((3000,1),dtype=int)*2020
    for i in range(19):
        year=np.append(year,(2019-i)*np.ones((3000,1),dtype=int))
    
    # generate variables
    variable_1 = np.random.normal(0, 1, 20*3000)
    variable_2 = np.random.normal(0, 1, 20*3000)
    # generate character
    character=np.random.normal(0,1,20*3000)
    # generate future return
    ret=character*-0.5+np.random.normal(0,1,20*3000)
    # create sample containing future return, character, time
    sample=np.array([character,year]).T
    
    breakpoints = ptfa().create_breakpoint(data=sample, number=4)
    print(breakpoints)
    
test_ptf_analysis()

#%% test class univariate()
def test_univariate() :
    '''
    TEST UNIVARIATE
    construct sample:
        1. 20 Periods
        2. 3000 Observations for each Period
        3. Divided into 10 groups with 9 breakpoints
        4. Character negative with return following the return=character*-0.5+sigma where sigma~N(0,1)
    '''
    import numpy as np
    from portfolio_analysis import Univariate as uni
    from portfolio_analysis import ptf_analysis as ptfa
    from util import plot
    
    # generate time 
    year=np.ones((3000,1),dtype=int)*2020
    for i in range(19):
        year=np.append(year,(2019-i)*np.ones((3000,1),dtype=int))
    
    # generate variables
    variable_1 = np.random.normal(0, 1, 20*3000)
    variable_2 = np.random.normal(0, 1, 20*3000)
    # generate character
    character=np.random.normal(0,1,20*3000)
    # generate future return
    ret=character*-0.5+np.random.normal(0,1,20*3000)
    # create sample containing future return, character, time
    sample=np.array([ret,character,year]).T

    # generate the Univiriate Class
    exper=uni(sample)
    exper.fit(4)
    # test function average_by_time
    data=exper.average_by_time()
    # test function summary_and_test
    exper.summary_and_test()
    # test function print_summary_by_time
    exper.print_summary_by_time()
    # test function print_summary
    exper.print_summary()

    # check breakpoint
    breakpoint = ptfa().create_breakpoint(data=np.array([character, year]).T, number=4)[0]
    exper = uni(sample)
    exper.fit(9, percn=breakpoint)
    exper.print_summary()
    
    print('-----EXPER NUMBER------:',exper.number)
    print(np.shape(exper.average_result))
    plot(exper)
    
    # generate factor
    factor=np.random.normal(0,1.0,(20,1))
    exper=uni(sample)
    exper.fit(9, maxlag=12)
    #exper.factor_adjustment(factor)
    # print(exper.summary_and_test())
    exper.print_summary()
    
    print('-------------------------------------------------------------------------------')
    # summary statstics
    exper.summary_statistics()
    exper.summary_statistics(periodic=True)
    exper.summary_statistics(variables=np.array([variable_1, variable_2]).T, periodic=True)
    
    # correlation 
    variable_3 = np.random.normal(0, 1, 20*3000)
    variable_4 = np.random.normal(0, 1, 20*3000)
    print('-------------------------------------- Correlation ---------------------------------')
    exper.correlation(variables=np.array([variable_1, variable_2, variable_3, variable_4]).T, periodic=True)
    exper.correlation(variables=np.array([variable_1, variable_2, variable_3, variable_4]).T)
    print(np.array([variable_1, variable_2, variable_3, variable_4]).T)

test_univariate()

# %% test class multiperiod univariate
def test_MultiPeriod_Univariate():
    '''
    TEST UNIVARIATE
    construct sample:
        1. 20 Periods
        2. 3000 Observations for each Period
        3. Divided into 10 groups with 9 breakpoints
        4. Character negative with return following the return=character*-0.5+sigma where sigma~N(0,1)
    '''
    import numpy as np
    import pandas as pd
    from portfolio_analysis import MultiPeriod_Univariate as muluni
    from portfolio_analysis import ptf_analysis as ptfa
    from util import plot
    
    # generate time 
    year=np.ones((3000,1),dtype=int)*2020
    for i in range(19):
        year=np.append(year,(2019-i)*np.ones((3000,1),dtype=int))
    
    year = pd.DataFrame(year, columns=['year'])

    # generate character
    character=pd.DataFrame(np.random.normal(0,1,20*3000))
    # generate future return
    ret1=character + np.random.normal(loc=0, scale=1, size=(20*3000,1))
    ret2=character + np.random.normal(loc=0, scale=1, size=(20*3000,1))
    # create sample containing future return, character, time
    ret_matrix = pd.merge(ret1, ret2, left_index=True, right_index=True)
    ret_matrix.columns = ['ret1', 'ret2']
    sample=pd.merge(character, year, left_index=True, right_index=True)
    sample.columns = ['character', 'year']

    # generate the Univiriate Class
    exper=muluni(ret_matrix, sample)
#    print(exper.ret_matrix)
    data = exper.fit(number=4, maxlag=0)

    print(exper.average_result)
    print(exper.ttest)
    print(np.shape(exper.ttest))
#    print(exper.params)
#    print(np.shape(data))
    exper.summary()
    print(exper.number)


    return data

test_MultiPeriod_Univariate()

# %% test class bivariate
def test_bivariate():
    '''
    TEST BIVARIATE
    construct sample:
        1. 20 Periods
        2. 3000 Observations for each Period
        3. Divided into 10 groups with 9 breakpoints
        4. first character negative with return following the return = character*-0.5 + sigma where sigma~N(0,1)
        5. second character positive with return following the return = character*0.5 + sigma where sigma~N(0,1) 
    '''

    import numpy as np
    from portfolio_analysis import Bivariate as bi
    from portfolio_analysis import ptf_analysis as ptfa
    
    # generate time 
    year = np.ones((3000,1), dtype=int)*2020
    for i in range(19):
        year = np.append(year, (2019-i)*np.ones((3000,1), dtype=int))
    
    # generate character
    character_1 = np.random.normal(0, 1, 20*3000)
    character_2 = np.random.normal(0, 1, 20*3000)

    # generate future return
    ret=character_1*-0.5 + character_2*0.5 + np.random.normal(0,1,20*3000)
    # create sample containing future return, character, time
    sample=np.array([ret,character_1, character_2, year]).T
    # generate the Univiriate Class
    exper=bi(sample)
    exper.fit(number=4)
    # test function divide_by_time
    group_by_time = exper.divide_by_time()
    print('group by time: \n', group_by_time)
    # test function average_by_time
    average_group_time = exper.average_by_time()
    print('average_group_time: \n', average_group_time)
    print('shape of average_group_time: \n', np.shape(average_group_time))
    # test function difference
    result = exper.difference(average_group_time)
    print('result :\n', result)
    print('difference matrix :\n', np.shape(result))
    # test function summary_and_test
    average, ttest = exper.summary_and_test()
    print('average :\n', average)
    print(' shape of average :', np.shape(average))
    print('ttest :\n', ttest)
    print('shape of ttest :', np.shape(ttest))
    # test function print_summary_by_time()
    exper.print_summary_by_time()
    # test function print_summary
    exper.print_summary()
    
    breakpoint = ptfa().create_breakpoint(np.array([character_1, character_2, year]).T, number=4)
    print('breakpoint\n', np.array([character_1, character_2, year]).T)
    percn_row = breakpoint[0]
    percn_col = breakpoint[1]
    exper = bi(sample)
    exper.fit(9, percn_row=percn_row, percn_col=percn_col)
    print('-------exper.result---------',exper.result)
    print('-------exper.result.shape---------',np.shape(exper.result))
    print('-------exper.num_row---------', exper.num_row)
    print('-------exper.num_col---------', exper.num_col)
    exper.print_summary()
    
    print('\n---------------------------------- Factor Adjustment--------------------------------------\n')
    # generate factor
    #factor = np.random.normal(0, 1.0, (20, 1))
    #exper = bi(sample, 9, maxlag=12)
    #exper.fit()
    #exper.factor_adjustment(factor)
    #exper.print_summary(export=True)

    print('\n---------------------------------- Conditinoal Portfolio ----------------------------------\n')
    # conditional portfolio
    # test function average_by_time
    exper_con = bi(sample)
    exper_con.fit(9, maxlag=12)
    average_group_time = exper_con.average_by_time(conditional=True)
    print('average_group_time: \n', average_group_time)
    print('shape of average_group_time: \n', np.shape(average_group_time))
    # test function difference
    result = exper_con.difference(average_group_time)
    print('result :\n', result)
    print('difference matrix :\n', np.shape(result))
    # test function summary_and_test
    average, ttest = exper_con.summary_and_test(conditional=True)
    print('average :\n', average)
    print(' shape of average :', np.shape(average))
    print('ttest :\n', ttest)
    print('shape of ttest :', np.shape(ttest))
    # test function print_summary_by_time()
    exper_con.print_summary_by_time()
    # test function print_summary
    exper_con.print_summary()
    

test_bivariate()

# %%
def test_multiperiod_bivariate():
    '''
    TEST UNIVARIATE
    construct sample:
        1. 20 Periods
        2. 3000 Observations for each Period
        3. Divided into 10 groups with 9 breakpoints
        4. Character negative with return following the return=character*-0.5+sigma where sigma~N(0,1)
    '''
    import numpy as np
    import pandas as pd
    from portfolio_analysis import MultiPeriod_Bivariate as mulbi
    from portfolio_analysis import ptf_analysis as ptfa
    from util import plot
    
    # generate time 
    year=np.ones((3000,1),dtype=int)*2020
    for i in range(19):
        year=np.append(year,(2019-i)*np.ones((3000,1),dtype=int))
    
    year = pd.DataFrame(year, columns=['year'])

    # generate character
    character_1 = pd.DataFrame(np.random.normal(0, 1, 20*3000))
    character_2 = pd.DataFrame(np.random.normal(0, 1, 20*3000))
    # generate future return
    ret1=   0.5 * character_1 - 0.5 * character_2 + np.random.normal(loc=0, scale=1, size=(20*3000,1))
    ret2= - 0.5 * character_1 + 0.5 * character_2 + np.random.normal(loc=0, scale=1, size=(20*3000,1))
    # create sample containing future return, character, time
    ret_matrix = pd.merge(ret1, ret2, left_index=True, right_index=True)
    ret_matrix.columns = ['ret1', 'ret2']
    sample=pd.merge(character_2, year, left_index=True, right_index=True)
    sample=pd.merge(character_1, sample, left_index=True, right_index=True)
    sample.columns = ['character_1', 'character_2', 'year']

    # generate the Univiriate Class
    exper=mulbi(ret_matrix, sample)
#    print(exper.ret_matrix)
    data = exper.fit(number=4, maxlag=12)

    print(exper.average_result)
    print(exper.ttest)
    print(np.shape(exper.ttest))
#    print(exper.params)
#    print(np.shape(data))
    exper.summary()
#    print(exper.number)

    breakpoint = ptfa().create_breakpoint(sample, number=4)
    percn_row = breakpoint[0]
    percn_col = breakpoint[1]
    exper = mulbi(ret_matrix, sample)
    exper.fit(9, percn_row=percn_row, percn_col=percn_col)
    exper.summary()

test_multiperiod_bivariate()

# %% test persistence
def test_persistence():
    '''
    This function is for testing persistence
    '''
    import numpy as np
    import pandas as pd
    from portfolio_analysis import Persistence as pste
    
    # generate time 
    year = np.ones((3000,1), dtype=int)*2020
    id = np.linspace(1, 3000, 3000, dtype=int)
    for i in range(19):
        year = np.append(year, (2019-i)*np.ones((3000,1), dtype=int))
        id = np.append(id, np.linspace(1, 3000, 3000, dtype=int))
    
    # generate character
    character_1 = np.random.normal(0, 1, 20*3000)
    character_2 = np.random.normal(0, 1, 20*3000)
    
    # generate future return
    ret=character_1*-0.5 + character_2*0.5 + np.random.normal(0,1,20*3000)
    # create sample containing future return, character, time
    sample = np.array([id, year, ret, character_1, character_2]).T
    sample = pd.DataFrame(sample, columns=['id', 'year', 'ret', 'character_1', 'character_2'])
    
    exper = pste(sample)
    exper.fit(lags=[1, 2, 3])
    exper.summary(periodic=True)
    exper.summary()

#    sample = sample.set_index(['id', 'year']).sort_index()
#    sample = sample.set_index([sample.columns[0], sample.columns[1]]).sort_index()
#    print(sample)
    
test_persistence()
# %% test tangency_portfolio
def test_tangency_portfolio():
    '''
    This function is for testing rangency_portfolio
    '''
    import numpy as np
    from portfolio_analysis import Tangency_portfolio as tanport

    mu = np.array([0.0427, 0.0015, 0.0285])
    cov_mat = np.mat([[0.01, 0.0018, 0.0011], [0.0018, 0.0109, 0.0026], [0.0011, 0.0026, 0.0199]])
    rf = 0.005

    portfolio = tanport(rf, mu, cov_mat)
    print(portfolio._portfolio_weight())
    print(portfolio.fit())
    portfolio.print()

    mu = np.array([0.0427, 0.0015, 0.0285, 0.0028])
    cov_mat = np.mat([[0.01, 0.0018, 0.0011, 0], [0.0018, 0.0109, 0.0026, 0], [0.0011, 0.0026, 0.0199, 0], [0, 0, 0, 0.1]])
    rf = 0.005

    portfolio = tanport(rf, mu, cov_mat)
    print(portfolio._portfolio_weight())
    print(portfolio.fit())
    portfolio.print()

test_tangency_portfolio()

# %% test Spanning test
def test_spanning_test():
    '''
    This function is for testing spanning test
    '''
    import numpy as np
    from portfolio_analysis import Spanning_test as span

    factor1 = np.random.normal(loc=0.1, scale=1.0, size=(240, 1))
    factor2 = np.random.normal(loc=0.2, scale=2.0, size=(240, 1))
    factor3 = np.random.normal(loc=0.5, scale=4.5, size=(240, 1))

    factor4 = 0.1 * factor1 + 0.5 * factor2 + 0.4 * factor3
    factor5 = -0.2 * factor1 - 0.1 * factor2 + 1.3 * factor3
    factor6 = 1.0 * factor1 - 0.5 * factor2 + 0.5 * factor3
    factor7 = 0.2 * factor1 + 0.1 * factor2 + 0.7 * factor3
    factor8 = -0.1 * factor1 -0.1 * factor2 + 1.2 * factor3
    factor9 = -0.3 * factor1 - 0.2 * factor2 + 1.5 * factor3
    factor10 = 0.9 * factor1 - 0.5 * factor2 + 0.6 * factor3
    factor11 = 0.2 * factor1 - 0.1 * factor2 + 0.9 * factor3
    
    factornew1 = np.random.normal(loc=0.3, scale=2.0, size=(240, 1))

    factork = np.block([factor1, factor2, factor3, factor4, factor5, factor6, factor7, factor8, factor9])
    factorn = np.block([factor10, factor11])

    model1 = span(factorn, factork)
    model1._regress()
    model1._build_statistics()
    model1.fit()
    model1.summary()

    model2 = span(factornew1, factork)
    model2._regress()
    model2._build_statistics()
    model2.fit()
    model2.summary()

test_spanning_test()


# %%
