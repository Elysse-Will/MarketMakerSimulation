import numpy as np
import matplotlib.pyplot as plt

#Define the parameters for the simulation 
# Number of trades executed
T = 2000
# The std devation of how much the mid price moves each step 
sigma = 0.01
#Proportion of informed traders in the market
alpha = 0.5
#Half-spread set by the market maker - difference between the bid and mid-point and the ask and mid-point
spread = 0.02
#Skewing factor for the market maker's quotes - how much the market maker adjusts their quotes based on inventory
gamma = [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007,0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05]


#Set a dictionary for the average pnl for each 100 runs at each gamma value 
PnL_results = {}
Cross_Sharpe = {}
Series_Sharpe = {}
Drawdown_results = {}
Run_results={}
#set loops to test different values of gamma
for g in gamma:
    print(f"\nRunning gamma = {g}")
    PnL_results[g] = []
    Cross_Sharpe[g] = []
    Series_Sharpe[g]=[]
    Drawdown_results[g]=[]
    Run_results[g]=[]

    #Run each simulation 100 times to get an average PnL for each value of gamma
    run_results = []
    ts_sharpes =[]
    inv_avg=[]
    max_drawdowns=[]
    for run in range(200):
        #Reset variables for each run
        mid = 100
        inventory = 0
        cash = 0
        PnL = []
        mid_prices = []
        skewed_mids = []
        inventories = []
        cash_positions = []
        
        
        for t in range(T):
    
            skewed_mid = mid - (g * inventory)
            skewed_mids.append(skewed_mid) 
            bid = skewed_mid - spread/2
            ask = skewed_mid + spread/2

            # Calculate move
            
            move = np.random.normal(0, sigma)


            # Trade executes at stale quotes
            if np.random.rand() < alpha:
                trade = 'buy' if move > 0 else 'sell'
                
            else:
                trade = 'buy' if np.random.choice([True, False]) else 'sell'

            if trade == 'buy':
                inventory -= 1
                cash += ask
            elif trade == 'sell':
                inventory += 1
                cash -= bid
            
            # Mid updates AFTER trade
            mid += move
            # MTM recorded at new mid
            mtm = cash + inventory * mid
            PnL.append(mtm)
            inventories.append(inventory)
            cash_positions.append(cash)
            cumulative = np.array(PnL)
            running_max= np.maximum.accumulate(cumulative)
            drawdown = cumulative - running_max
            max_drawdowns.append(np.min(drawdown))

        if inventory != 0:
            cash += inventory * mid
            inventory = 0
        # Update the final PnL to reflect the zero inventory position
        inv = np.mean(np.abs(inventories))
        inv_avg.append(inv)
        PnL[-1] = cash 
        pnl_changes = np.diff(PnL)
        ts_sharpe = np.mean(pnl_changes)/np.std(pnl_changes)
        ts_sharpes.append(ts_sharpe)
        run_results.append(PnL[-1])
        Run_results[g].append(PnL[-1])
         

    PnL_results[g] = (np.mean(run_results))
    Cross_Sharpe[g] = (np.mean(run_results)/np.std(run_results))
    Series_Sharpe[g] = (np.mean(ts_sharpes))
    Drawdown_results[g] = np.mean(max_drawdowns)
# Take the average inventory across the runs to find the theoretical optimum gamma 
    print(f"Avg Max Drawdown: {Drawdown_results[g]:.2f}")


fig, ax = plt.subplots(figsize=(10, 12))
ax.plot(gamma,[Drawdown_results[g] for g in gamma], color='blue')
ax.set_title('Average Maximum Drawdown vs Gamma')
ax.set_xlabel('Gamma')
ax.set_ylabel('Average Maximum Drawdown')
ax.grid(True)
plt.show()

