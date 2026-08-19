#Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt

#Define the parameters for the simulation 
# Number of trades executed
T = 10000
# The std devation of how much the mid price moves each step 
sigma = 0.01
#Proportion of informed traders in the market
alpha = 0.1
#Half-spread set by the market maker - difference between the bid and mid-point and the ask and mid-point
spread = 0.02
#Skewing factor for the market maker's quotes - how much the market maker adjusts their quotes based on inventory
gamma = 0.01
#Assign a maximum inventory limit
max_inventory = 50
#Arrays to store the mid price, inventory, PnL and cash over time for plotting
PnL_10_runs =[]

#Set the loop to run ten times 
for run in range(10):
    # Reset variable lists for each run 
    mid = 100.0
    inventory = 0
    cash = 0
    PnL = []
    mid_prices = []
    skewed_mids =[]
    inventories = []
    cash_positions = []

    # Execute the trades for each run 
    for t in range(T):
        # Set the skewed mid - inventory specific mid to shift quotes to aid settling positions 
        skewed_mid = mid - (gamma * inventory)
        skewed_mids.append(skewed_mid) 

        #Set the bid and the ask price based on the set spread and the skewed mid 
        bid = skewed_mid - spread/2
        ask = skewed_mid + spread/2

        # Calculate move - random price change at each stage 
        move = np.random.normal(0, sigma)

        # Trade executes at stale quotes
        # If the trader is imformmed 
        if np.random.rand() < alpha:
            trade = 'buy' if move > 0 else 'sell'
           # if trader is uninformed then 50/50 move 
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
        mid_prices.append(mid)

        # MTM recorded at new mid
        mtm = cash + inventory * mid
        PnL.append(mtm)
        inventories.append(inventory)
        cash_positions.append(cash)

    # Code the closeout of the simulation to end on zero position
    if inventory != 0:
        cash += inventory * mid
        inventory = 0
    # Update the final PnL to reflect the zero inventory position
    PnL[-1] = cash  
    
    PnL_10_runs.append(PnL)


fig, ax = plt.subplots(figsize=(10, 6))
for i, PnL in enumerate(PnL_10_runs):
    ax.plot(range(T), PnL, label=f'Run {i+1}')
ax.set_title('PnL over Trades - Market Making Strategy (10 Runs)')
ax.set_xlabel('Trades')
ax.set_ylabel('PnL')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('Pnl_10_Runs.png')
plt.show()

print (f"Final PnL: {PnL[-1]:.2f}")
print(f"Final Inventory: {inventory} Shares")
print(f"Final Cash: {cash:.2f}")
print(f"Total trades executed: {T} trades")

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

ax1.plot(range(T), PnL, label='PnL', color='blue')
ax1.set_title('PnL over Time - Market Making Strategy')
ax1.set_ylabel('PnL')
ax1.legend()
ax1.grid(True)

ax2.plot(range(T), inventories, label='Inventory', color='red')
ax2.set_title('Inventory over Time - Market Making Strategy')
ax2.set_ylabel('Inventory')
ax2.legend()
ax2.grid(True)

ax3.plot(range(T), cash_positions, label='Cash', color='green')
ax3.set_title('Cash Position over Time - Market Making Strategy')
ax3.set_ylabel('Cash')
ax3.legend()
ax3.grid(True)

ax4.plot(range(T), mid_prices, label='Mid Prices', color='blue')
ax4.plot(range(T), skewed_mids, label='Skewed Mids', color='orange')
ax4.set_title('Mid Prices vs Skewed Mids - Market Making Strategy')
ax4.set_xlabel('Time')
ax4.set_ylabel('Price')
ax4.legend()
ax4.grid(True)

plt.tight_layout()
plt.savefig('Market_Making_Strategy.png')
plt.show()