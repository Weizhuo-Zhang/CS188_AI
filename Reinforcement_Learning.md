---
marp: true
---

# Reinforcement Learning

What if we **don't know**
- $P$: Transitions
- $r$: Reward function

Why Q-Value

---
## Q-Learning
1. Initialize $Q(s,a)$ arbitrarily.
2. For each episode:
   Initialize $s$ (go to the initial state)
   Repeat each step in the episode
      Select the next action $a$ to apply from s(using e.g. episilon greedy, UCT) use $Q(s,a)$
      Execute the action a$ and observe the reward $r$ and new state $s'$
      $Q(s,a)=Q(s,a)+\alpha\left[r+\gamma V(s')(???)-Q(s,a)\right]$
      $s=s'$
   Until $s$ is terminal.

---
## SARSA

---