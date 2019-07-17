# Reinforcement Learning

## Active Reinforcement Learning

Active Reinforcement Learning collects data while learning from Q-Values.

Full reinforcement learning: optimal policies (like value iteration)
- You don't know the transitions T(s,a,s')
- You don't know the rewards R(s,a,s')
- You choose the actions now
- **Goal: learn the optimal policy / values**

In this case:
- Learner makes choices!
- Fundamental tradeoff: exploration vs. exploitation
- This is NOT offline planning! You actually take actions in the world and find out what happens...

## Detour: Q-Value Interation
Value iteration: find successive (depth-limited) values
- Start with V<sub>0</sub>(s)=0, which we know is right
- Given V<sub>k</sub>, calculate the depth k+1 values for all states:

$Vk+1=$
