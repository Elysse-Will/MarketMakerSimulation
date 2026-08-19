# MarketMakerSimulation
Motivation

Market makers provide the liquidity to the markets and generate profit through their spreads but are doing so against risks. Within this project we have looked at two prevalent risks within market making and have related a simulation to that of the Avellaneda – Stoikov theoretical optimum gamma.

The first risk investigated is that of adverse selection – informed traders have prior information of market movements and can make hits against the market maker for profit.

The second is inventory risk when a market maker holds a large, long or short position they are liable to the risk associated with exposure to price movements. The more time held in this position can lead to potential for more catastrophic loss.

This project looks to show the fundamental building of the market maker activity and zooming into the effects of growing proportions of informed traders and the possible risk aversion methods for this exposure.

The Avellaneda-Stoikov framework highlights the impact of adjustment of market mid pricing with regards to the stock inventory size held by the agent by solving for optimal bid/ask spreads given inventory, volatility and risk aversion. Within this project we will specifically look at how an empirically calibrated gamma can maximise risk adjusted returns through a Monte Carlo simulation.

Method

The Avellandeda-Stoikov paper defined mid-price of the stock using continuous Brownian motion to denote the infinitely changing price and used it to obtain closed-form formulas for the reservation price.

𝑑
𝑆
𝑢
=
𝜎
 
𝑑
𝑊
𝑢
dS
u
	​

=σdW
u
	​


However, when implementing the numerical solutions, they had to discretise the continuous process to produce results noting the trade-off between the time step being small enough to avoid multiple orders but large enough so that there is no risk of not seeing orders (Section 3.3). This project follows a similar approach through modelling the mid-price as a discrete-time random step dictated by sigma, representing the standard deviation of the pricing increment, a discretised simulation of the paper's continuous sigma.

𝑆
𝑡
+
1
=
𝑆
𝑡
+
𝜀
𝑡
,
𝜀
𝑡
∼
𝑁
(
0
,
𝜎
2
)
S
t+1
	​

=S
t
	​

+ε
t
	​

,ε
t
	​

∼N(0,σ
2
)

A further decision was made to implement the finite horizon version of the Avellandeda-Stoikov model which includes a forced flat close out at ending time 
𝑇
T (Section 2.2). This choice was made over the alternative infinite horizon formulation in which a discount rate is used to discount the value of future outcomes indefinitely (Section 2.3) rather than providing a fixed end to the trading session.

The trading mechanism was a further distinction that this project adjusted from the Avellaneda – Stoikov paper. The paper includes both a "frozen inventory" passive agent who holds a fixed position and doesn't trade and an active agent posting bid and ask quotes that are filled according to a distance dependant Poisson intensity governed by the parameter 
𝑘
k.

𝜆
(
𝛿
)
=
𝐴
𝑒
−
𝑘
𝛿
λ(δ)=Ae
−kδ

This project sits in the mid-point between both trading mechanisms as the trades are conducted live and continuous throughout the simulation using a fixed spread rather than a static position until the deadline time. However, the decision of where to centre that spread is taken from the frozen-inventory reservation price formula which is calculated at each time step as the inventory evolves throughout the simulation.

𝑟
(
𝑠
,
𝑞
,
𝑡
)
=
𝑠
−
𝑞
𝛾
𝜎
2
(
𝑇
−
𝑡
)
r(s,q,t)=s−qγσ
2
(T−t)

Within this project while the paper uses a distance dependant fill probability which states how likely your bid and ask are to be hit dependant on the distance of the pricing from the mid pricing, this project instead assumes that a trade will always occur at each step but the favourability of that trade is determined by the parameter alpha (adverse selection risk). This distinguishes whether the trader is informed and the trade is aligned with upcoming price movement or an uninformed trader with a random direction.

This project's bid and ask quotes are set using the mid-price before that steps price movement occurs, trades are executed on stale quotes, and the mid-price is updated after. This was a purposeful implementation to simulate informed trades genuinely exploiting a timing disadvantage mirroring the concept of informed trades through latency arbitrage.

Gamma is the projects parameter representing inventory risk as it controls quote skewing in response to inventory levels.

skewed_mid
𝑡
=
mid
𝑡
−
𝛾
⋅
inventory
𝑡
skewed_mid
t
	​

=mid
t
	​

−γ⋅inventory
t
	​


Avellaneda-Stoikov's gamma instead is a risk-aversion coefficient which is absorbed alongside the paper's sigma squared and 
(
𝑇
−
𝑡
)
(T−t) term into a single empirically calibrated constant.

𝛾
project
≡
𝛾
⋅
𝜎
2
⋅
(
𝑇
−
𝑡
)
γ
project
	​

≡γ⋅σ
2
⋅(T−t)

However, it's important to note that the nature of the 
(
𝑇
−
𝑡
)
(T−t) coefficient is explicitly time varying which in the paper means the skewing naturally tapers as the end of the trading session approaches. In this project gamma is a fixed constant meaning the skewing is implemented with equal intensity throughout the trading session. A market maker would likely reduce the inventory driven skewing once there is little time remaining for that inventories price to move against the position held even if that position is large.
