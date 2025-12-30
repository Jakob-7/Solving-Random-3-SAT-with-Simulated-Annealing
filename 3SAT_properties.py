import numpy as np
import matplotlib.pyplot as plt
from KSAT import KSAT
from SimAnn import simann

## Compute P(N, M) for given N and varying M.
def compute_pnm(N, M_values, K, n_instances, mcmc_steps, anneal_steps, beta0, beta1, seed=42):
    np.random.seed(seed)
    P_N_M = []

    for M in M_values:
        solved_count = 0
        for _ in range(n_instances):
            # Generate a random 3-SAT instance
            ksat = KSAT(N, M, K, seed=np.random.randint(0, 1e6))
            # Run Simulated Annealing
            best = simann(ksat, mcmc_steps=mcmc_steps, anneal_steps=anneal_steps,
                          beta0=beta0, beta1=beta1, seed=np.random.randint(0, 1e6))
            # Check if the solution is valid (cost == 0)
            if best.cost() == 0:
                solved_count += 1
        # Compute empirical probability
        P_N_M.append(solved_count / n_instances)

    return P_N_M

# Parameters
N = 200
M_values = [400, 500, 600, 700, 800, 900, 1000]
K = 3
n_instances = 30
mcmc_steps = 500
anneal_steps = 10
beta0 = 1.0
beta1 = 10.0

### Exercise 1: Compute P(N, M)
P_N_M = compute_pnm(N, M_values, K, n_instances, mcmc_steps, anneal_steps, beta0, beta1)

# Plot P(N, M) vs M
plt.figure(figsize=(8, 6))
plt.plot(M_values, P_N_M, marker='o', label=f"N={N}")
plt.axhline(0.5, color='r', linestyle='--', label="P(N, M) = 0.5")
plt.xlabel("Number of Clauses (M)")
plt.ylabel("Empirical Probability P(N, M)")
plt.title("Empirical Probability of Solving 3-SAT")
plt.legend()
plt.grid()
plt.savefig("PNM_vs_M.png")
plt.show()

### Exercise 2: Find the value of the algorithmic threshold
from scipy.interpolate import interp1d
threshold = interp1d(P_N_M, M_values)(0.5)
print(threshold)

### Exercise 3: Repeat for multiple values of N
N_values = [300, 400, 500, 600]
results = {}
for N in N_values:
    results[N] = compute_pnm(N, M_values, K, n_instances, mcmc_steps, anneal_steps, beta0, beta1)

# Plot P(N, M) for different values of N
plt.figure(figsize=(10, 7))
for N in N_values:
    plt.plot(M_values, results[N], marker='o', label=f"N={N}")
plt.axhline(0.5, color='r', linestyle='--', label="P(N, M) = 0.5")
plt.xlabel("Number of Clauses (M)")
plt.ylabel("Empirical Probability P(N, M)")
plt.title("Empirical Probability for Different N")
plt.legend()
plt.grid()
plt.savefig("PNM_vs_M_for_N.png")
plt.show()

# Find the values of the algorithmic threshold
from scipy.interpolate import interp1d
thresholds = {}
for N in N_values:
    P_N_M = results[N]
    try:
        thresholds[N] = float(interp1d(P_N_M, M_values)(0.5))
    except ValueError:
        thresholds[N] = None

for N, threshold in thresholds.items():
    if threshold is not None:
        print(f"The algorithmic threshold for N={N} is M={threshold:.2f}")
    else:
        print(f"The algorithmic threshold for N={N} could not be determined.")

## Rescale M by N and plot P(N, M) vs M/N
results[200] = compute_pnm(200, M_values, K, n_instances, mcmc_steps, anneal_steps, beta0, beta1)
N_values = [200] + N_values

plt.figure(figsize=(10, 7))
for N in N_values:
    rescaled_M = [M / N for M in M_values]
    plt.plot(rescaled_M, results[N], marker='o', label=f"N={N}")

plt.axhline(0.5, color='r', linestyle='--', label="P(N, M) = 0.5")
plt.xlabel("Rescaled Clauses (M/N)")
plt.ylabel("Empirical Probability P(N, M)")
plt.title("Empirical Probability as a Function of M/N")
plt.legend()
plt.grid()
plt.savefig("PNM_vs_Rescaled_M_for_N.png")
plt.show()

