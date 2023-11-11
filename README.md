# portfolio-monte-carlo-sim

This algorithm runs a Monte Carlo simulation to approximate the probability of
different growth outcomes of a given portfolio, using the historical data of 
the portfolio's assets. Every simulated year, each asset's return is randomly
picked from the asset's historical returns. This is repeated for a specified
number of years, and the whole process is repeated for many trials. These
virtual simulations of the portfolio allow us to approximate the
probability of different growth outcomes *assuming historical data reflects
future performance*.
The historical data of the assets is accessed using the yfinance module, which
is a free unofficial API to access data from Yahoo Finance.

How to Use the Simulator: 
There will be commented headers in the code with numbers matching the steps below. They will also say 'USER INPUT HERE >>>' to indicate that the user can modify parameters in that section of the code.
 1) First create variables to represent the assets you wish to include in your
    portfolio. The yfinance module allows to do so by calling its Ticker 
    method and including the ticker of the asset as it appears on Yahoo Finance. Use the form [asset_variable_name] = yf.Ticker('[yahoo ticker name of asset]')
 2) Build your portfolio using a dictionary with the key being an asset from the asset variables created in Step 1), and the
    value being the weight of that asset in the portfolio (represented as a
    number between 0 and 1).
 3) Set up the simulation by specifying how many years to simulate, how many
    trials to run, which portfolio to use, and what the initial invested amount
    is. The simulation of the portfolio for the specified period of years is 
    repeated for many trials to record a vast amount of possible outcomes.
 4) (Optional) Select the historical annualized return of a benchmark 
    (the default is 11.88% of the SP500). The program will calculate how often
    the simulated portfolio outperforms the benchmark's future 
    value at the end of the simulation period.
 5) Run the program. Once the program ends, it will display a graph showing the
    growth of all the simulated portfolios as well as the distribution of the
    growth outcomes. The program will also print some statistics such as the
    mean, median, and range of the growth outcomes.
 6) If you wish to know the probability that the portfolio grows within a 
    certain range, or either above or below a certain threshold, use the 
    function growth_probaility() as per its docstring.

 Assumptions to keep in mind:
 - The simulation assumes that the portfolio is rebalanced every year.
 - The simulation assumes that historical data reflects future performance.
   Keep in mind that this is not always the case. Also keep in mind that some 
   assets' historical data spans shorter periods of time and this may bias the 
   simulation results (cryptocurrencies have this issue).
