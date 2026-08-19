import numpy as np
import matplotlib.pyplot as plt

#Define the parameters for the simulation 
# Number of trades executed
T = 20000
# The std devation of how much the mid price moves each step 
sigma = 0.01
#Proportion of informed traders in the market
alpha = [0.1, 0.3, 0.5, 0.7, 0.9]
#Half-spread set by the market maker - difference between the bid and mid-point and the ask and mid-point
spread = 0.02
#Skewing factor for the market maker's quotes - how much the market maker adjusts their quotes based on inventory
gamma = [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007,0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05]


#Set a dictionary for the average pnl for each 100 runs at each gamma value 
PnL_results = {}
Sharpe = {}
#set loops to test different values of gamma
for a in alpha:
    print(f"\nRunning alpha = {a}")
    PnL_results[a] = {}
    Sharpe[a] = {}
    for g in gamma:
        print(f"\nRunning gamma = {g}")
        run_results = []
        
        for run in range(100):
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
                if np.random.rand() < a:
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
            if inventory != 0:
                cash += inventory * mid
                inventory = 0
            # Update the final PnL to reflect the zero inventory position
            
            PnL[-1] = cash 
            run_results.append(PnL[-1]) 
        
        PnL_results[a][g] = (np.mean(run_results))
        Sharpe[a][g] = (np.mean(run_results)/np.std(run_results))


fig, (ax) = plt.subplots(figsize=(10, 12))

for a in alpha:
    sharpe= [Sharpe[a][g] for g in gamma]
    ax.plot(gamma,sharpe, label= f'alpha = {a}')

ax.set_xlabel('Gamma')
ax.set_ylabel('Cross-Simulation Sharpe Ratio')
ax.set_title('Sharpe vs Gamma at Different Alpha Values')
ax.legend()
ax.grid(True)

plt.show()
