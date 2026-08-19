import numpy as np
import matplotlib.pyplot as plt

#Define the parameters for the simulation 
# Number of trades executed
T = 20000
# The std devation of how much the mid price moves each step 
sigma = 0.01
#Proportion of informed traders in the market
alpha = 0.5
#Half-spread set by the market maker - difference between the bid and mid-point and the ask and mid-point
spread = 0.02
#Skewing factor for the market maker's quotes - how much the market maker adjusts their quotes based on inventory
gamma = [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007,0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05]
max_inventory = 150 

#Set a dictionary for the average pnl for each 100 runs at each gamma value 
PnL_results = {}
Cross_Sharpe = {}
Series_Sharpe = {}
Run_results={}
#set loops to test different values of gamma
for g in gamma:
    print(f"\nRunning gamma = {g}")
    PnL_results[g] = []
    Cross_Sharpe[g] = []
    Series_Sharpe[g]=[]
    Run_results[g]=[]

    #Run each simulation 100 times to get an average PnL for each value of gamma
    run_results = []
    ts_sharpes =[]
    inv_avg=[]
    for run in range(500):
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

            if trade == 'buy' and inventory > -max_inventory:
                inventory -= 1
                cash += ask
            elif trade == 'sell' and inventory < max_inventory:
                inventory += 1
                cash -= bid
            
            # Mid updates AFTER trade
            mid += move
            # MTM recorded at new mid
            mtm = cash + inventory * mid
            PnL.append(mtm)
            inventories.append(inventory)
            cash_positions.append(cash)
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
# Take the average inventory across the runs to find the theoretical optimum gamma 
    print(f"Avg Inv {np.mean(inv_avg):.2f}")

    print(f" Average P&L: {np.mean(run_results):.2f} Series Sharpe: {np.mean(ts_sharpes):.4f} Cross-sectional Sharpe: {np.mean(run_results)/np.std(run_results):.2f}")


fig, (ax, ax1,ax2) = plt.subplots(3,1,figsize=(10, 12))
ax.plot(gamma,[PnL_results[g] for g in gamma], color='blue')
ax.set_title('P&L vs Gamma — Market Making Strategy')
ax.set_ylabel('P&L')
ax.grid(True)

ax1.plot(gamma,[Cross_Sharpe[g] for g in gamma], color = 'red')
ax1.set_title('Cross-Simulation Sharpe vs Gamma — Market Making Strategy')
ax1.set_ylabel('Cross-Simulation Sharpe')
ax1.grid(True)

ax2.plot(gamma, [Series_Sharpe[g] for g in gamma], color = 'black')
ax2.set_title('Time-Series Sharpe vs Gamma — Market Making Strategy')
ax2.set_xlabel('Gamma')
ax2.set_ylabel('Time-Series Sharpe')
ax2.grid(True)

plt.show()

all_data = Run_results[0] + Run_results[0.004]
bin_edges = np.linspace(min(all_data), max(all_data), 31)


fig, ax3 = plt.subplots(figsize=(10, 6))
plt.hist(Run_results[0], bins=bin_edges, alpha=0.5, label='Gamma = 0', color='green', edgecolor='black')
plt.hist(Run_results[0.004], bins=bin_edges, alpha=0.5, label='Optimum Gamma = 0.004', color='orange', edgecolor='black')
plt.xlabel('Final P&L')
plt.ylabel('Frequency')
plt.title('Distribution of Final P&L: No Skewing vs Optimal Gamma')
plt.legend()
plt.grid(True)
plt.show()
