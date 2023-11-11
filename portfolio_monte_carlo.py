import yfinance as yf
import matplotlib.pyplot as plt
import random
import statistics as sta
import numpy as np


# --- MONTE CARLO PORTFOLIO SIMULATOR --- #
# This algorithm runs a Monte Carlo simulation to approximate the probability of
# different growth outcomes of a given portfolio, using the historical data of 
# the portfolio's assets. Every simulated year, each asset's return is randomly
# picked from the asset's historical returns. This is repeated for a specified
# number of years, and the whole process is repeated for many trials. These
# virtual simulations of the portfolio allow us to approximate the
# probability of different growth outcomes *assuming historical data reflects
# future performance*.
# The historical data of the assets is accessed using the yfinance module, which
# is a free unofficial API to access data from Yahoo Finance.

# How to Use the Simulator: (See matching numbers to steps in code below)
# 1) First create variables to represent the assets you wish to include in your
#    portfolio. The yfinance module allows to do so by calling its Ticker 
#    method and including the ticker of the asset as it appears on Yahoo Finance.
# 2) Build your portfolio using a dictionary with the key being an asset and the
#    value being the weight of that asset in the portfolio (represented as a
#    number between 0 and 1).
# 3) Set up the simulation by specifying how many years to simulate, how many
#    trials to run, which portfolio to use, and what the initial invested amount
#    is. The simulation of the portfolio for the specified period of years is 
#    repeated for many trials to record a vast amount of possible outcomes.
# 4) (Optional) Select the historical annualized return of a benchmark 
#    (the default is 11.88% of the SP500). The program will calculate how often
#    the portfolio's simulations outperform the benchmark's expected future 
#    value.
# 5) Run the program. Once the program ends, it will display a graph showing the
#    growth of all the simulated portfolios as well as the distribution of the
#    growth outcomes. The program will also print some statistics such as the
#    mean, median, and range of the growth outcomes.
# 6) If you wish to know the probability that the portfolio grows within a 
#    certain range, or either above or below a certain threshold, use the 
#    function growth_probaility() as per its docstring.

# Assumptions to keep in mind:
# - The simulation assumes that the portfolio is rebalanced every year.
# - This simulation assumes that historical data reflects future performance.
#   Keep in mind that this is not always the case. Also keep in mind that some 
#   assets' historical data spans shorter periods of time and this may bias the 
#   simulation results (cryptocurrencies have this issue).

# Ideas to Add:
# - Trading fees, dividends, monthly contributions & withdrawals.
# - Simulate a benchmark portfolio or index to compare performance of main
#   portfolio (quantify out- or under-performance using standard deviation/
#   tracking error).


# 1) DEFINE ASSETS (USER INPUT HERE >>>)
# <variable_name> = yf.Ticker('<ASSET TICKER ON YAHOO>')
aapl = yf.Ticker('AAPL')
ia_daq = yf.Ticker('0P0000ZEJ5.TO')
btc = yf.Ticker('BTC-USD')
eth = yf.Ticker('ETH-USD')

ndx = yf.Ticker('^NDX')


# 2) BUILD PORTFOLIOS (USER INPUT HERE >>>)
# <portfolio_name> = {<asset_variable> : <weight>} (note that 0 < weight < 1)
portfolio1 = {ia_daq:0.7, aapl:0.24, btc:0.03, eth:0.03}
portfolio2 = {ia_daq:0.7, aapl:0.3}


# 3) SIMULATION PARAMETERS (USER INPUT HERE >>>)
TRIALS = 1000
YEARS_TO_SIMULATE = 10
PORTFOLIO = portfolio2
INITIAL_INVESTMENT = 100


# 4) BENCHMARK RETURN (USER INPUT HERE >>>)
BENCHMARK_ANNUAL_RETURN = 11.88 / 100 # SP500 historical average return
benchmark_future_value = INITIAL_INVESTMENT * (1 + BENCHMARK_ANNUAL_RETURN) \
    ** YEARS_TO_SIMULATE  # Value of the benchmark at the end of the simulation period


# FUNCTIONS #
def get_yearly_returns(asset: object) -> list:
    """ Return a list with all recorded yearly returns of an asset.
    
    >>> get_yearly_returns(btc)
    [0.3447108315183143, 1.2383113710651474, 13.688978981270699, ...]
    """
    
    data = asset.history('max').Close.resample('Y').ffill().pct_change()
    data = [value for value in data]
    data.pop(0) # Remove the first value which is nan
    
    return data

def growth_probability(growth_data, min_growth_pct: float, max_growth_pct: float) -> float:
    """ Return the percentage of monte carlo trials that resulted in a
    portfolio growth within the range min_growth_pct to max_growth_pct, 
    inclusive.
    If min_growth_pct == None, return the percentage of trials that resulted in
    a growth equal to or below max_growth_pct.
    If max_growth_pct == None, trutn the percentage of trials that resulte in a
    growth equal to or above min_growth_pct.
    
    Preconditions: 
    - min_growth_pct >= max_growth_pct
    - min_growth_pct and max_growth_pct are expressed in percentage
    - growth_data contains growth data of PORTFOLIO, in percentage, following a
      Monte Calro simulation of TRIALS trials. In this code, the variable 
      final_growths holds this data, so use that as the first argument.
    
    >>> growth_probability(final_growths, 0, 100)
    4.9
    >>> growth_probability(final_growths, None, 0)
    0.3
    >>> growth_probability(final_growths, 100, None)
    94.8
    """
    
    count = 0
    
    if min_growth_pct == None and max_growth_pct != None:
        for growth in growth_data:
            if growth < max_growth_pct:
                count += 1
         
    elif min_growth_pct != None and max_growth_pct == None:
        for growth in growth_data:
            if growth > min_growth_pct:
                count += 1
    else:
        for growth in growth_data:
            if min_growth_pct < growth < max_growth_pct:
                count += 1
    
    return count / len(growth_data) * 100


# MONTE CARLO SIMULATION #
# Store assets data for each asset in portfolio (saves computation time)
yearly_returns = {}
for asset in PORTFOLIO.keys():
    yearly_returns[asset.ticker] = get_yearly_returns(asset)

data = []

for _ in range(TRIALS):
    current_sim_data = []
    portfolio_value = 0
    
    for year in range(YEARS_TO_SIMULATE + 1):
        value_to_add = 0
        
        for asset in PORTFOLIO:
            weight = PORTFOLIO[asset]
            
            if year == 0:
                portfolio_value += INITIAL_INVESTMENT * weight
            else:
                asset_value = portfolio_value * weight # Portfolio is rebalanced
                random_return = random.choice(yearly_returns[asset.ticker])
                value_to_add += asset_value * random_return
        
        portfolio_value += value_to_add
        current_sim_data.append(portfolio_value)
    
    data.append(current_sim_data)
                

# VISUALIZE RESULTS # 
fig, ax = plt.subplots(2) 

# Plot all simulated portfolios over time
for sim_data in data:
    
    # Convert yearly portfolio values to % increase from start of the simulation
    sim_data = np.array(sim_data) 
    sim_data = (sim_data - INITIAL_INVESTMENT) / INITIAL_INVESTMENT * 100
    
    ax[0].plot(sim_data)
    
ax[0].set_xlabel('Years')
ax[0].set_ylabel('Portfolio Value Increase (%)')

# Plot distribution of final portfolio growths (x = growth %, y = frequency %)
final_growths = [sim_data[-1] / INITIAL_INVESTMENT * 100 - 100 for sim_data in data]
final_growth_counts = [final_growths.count(value) for value in final_growths]
final_growth_frequencies = np.array(final_growth_counts) / TRIALS * 100

ax[1].hist(final_growths, weights = final_growth_frequencies, bins = 100)
ax[1].set_xlabel('Final Growth (%)')
ax[1].set_ylabel('Frequency (%)')

# Print relevant statistics
print('>>> Portfolio Growth Data: <<<')
print(f'Mean: {round(sta.mean(final_growths), 2)}%')
print(f'Median: {round(sta.median(final_growths), 2)}%')
print(f'Range: {round(min(final_growths), 2)}% to {round(max(final_growths), 2)}%')

outperformance_probability = growth_probability(final_growths, benchmark_future_value, None)
print(f'Probability of outperforming benchmark: {round(outperformance_probability, 2)}%')

plt.show()
