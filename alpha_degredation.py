#Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt

#Define the parameters for the simulation 
# Number of trades executed
T = 20000
# The std devation of how much the mid price moves each step 
sigma = 0.01
#Proportion of informed traders in the market
alpha = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
#Half-spread set by the market maker - difference between the bid and mid-point and the ask and mid-point
spread = 0.02
#Skewing factor for the market maker's quotes - how much the market maker adjusts their quotes based on inventory
gamma = 0.01

max_inventory = 300
Pnl_results = []
Inventory_results = []
    #Run each simulation 100 times to get an average PnL for each value of alpha
for a in alpha:
    print(f"Running alpha = {a}")
    run_results = []
    Avg_inv = []
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
        
            
            skewed_mid = mid - (gamma * inventory)
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
        PnL[-1] = cash 
        Avg_inv.append(np.mean(np.abs(inventories)))
        run_results.append(PnL[-1])
    Inventory_results.append(np.mean(Avg_inv))
    Pnl_results.append(np.mean(run_results))      



fig, (ax,ax1) = plt.subplots(2,1,figsize=(12, 6))
ax.plot(alpha, Pnl_results,color='blue')
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
ax.axvline(x=0.5, color='grey', linestyle='--', linewidth=0.8, label='Theoretical break-even')
ax.set_title('P&L vs Alpha — Market Making Strategy')
ax.set_xlabel('Alpha')
ax.set_ylabel('P&L')
ax.legend()
ax.grid(True)

ax1.plot(alpha, Inventory_results,color='red')
ax1.set_title('Inventory vs Alpha — Market Making Strategy')
ax1.set_xlabel('Alpha')
ax1.set_ylabel('Inventory')
ax1.grid(True)

plt.show()




