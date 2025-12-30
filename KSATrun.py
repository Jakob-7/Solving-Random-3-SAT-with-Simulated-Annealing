import SimAnn
import KSAT
import numpy as np
import matplotlib.pyplot as plt


## exercise 2 (K-SAT instance with N=200 variables and M=200 Clauses)
# After experiencing around a bit, I decided to use the following parameters (explanations in the report)
N,M,K,seed = 200, 200, 3, 42
mcmc_steps, anneal_steps, beta0, beta1=500, 10, 1.0, 10.0


#Run KSAT
ksat = KSAT.KSAT(N,M,K, seed=seed)

best = SimAnn.simann(ksat,
                      mcmc_steps =mcmc_steps, anneal_steps = anneal_steps,
                      beta0 = beta0, beta1 = beta1,
                      seed = seed,
                      debug_delta_cost = True) 


# Plotting the evolution of the acceptance rate during the annealing schedule
beta_list = [*np.linspace(beta0, beta1, anneal_steps - 1), float('inf')]
acceptance_rates = []

# Acceptance Rate Tracking
for beta in beta_list:
    accepted = 0
    for _ in range(mcmc_steps):
        move = ksat.propose_move()
        delta_c = ksat.compute_delta_cost(move)
        if delta_c <= 0 or np.random.rand() < np.exp(-beta * delta_c):
            ksat.accept_move(move)
            accepted += 1
    acceptance_rates.append(accepted / mcmc_steps)

# Plot acceptance rate evolution
plt.text(1.05, max(acceptance_rates), 
         f"N={N}, M={M}, mcmc_steps={mcmc_steps}, anneal_steps={anneal_steps}, β0={beta0}, β1={beta1}",
         fontsize=10, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.8))
plt.plot(beta_list[:-1], acceptance_rates[:-1], marker='o')
plt.xlabel("Inverse Temperature (Beta)")
plt.ylabel("Acceptance Rate")
plt.title("Acceptance Rate During Annealing")
plt.grid()
plt.show()


