# Solving Random 3-SAT with Simulated Annealing

This repository contains a computer programming project focused on solving **random 3-SAT instances** using **Simulated Annealing**, and on empirically studying the **algorithmic phase transition** of the 3-SAT problem.

The project combines algorithm implementation, performance analysis, and complexity-theoretic insights.

---

## 🎯 Problem Overview

The **k-SAT problem** is a canonical **NP-complete** problem in computer science.

Given a Boolean formula in conjunctive normal form with k literals per clause, the goal is to determine whether there exists an assignment of variables that satisfies all clauses.

This project investigates:
- The effectiveness of **Simulated Annealing (SA)** as a heuristic solver for random 3-SAT
- How the probability of solving instances depends on the number of clauses
- The existence of an **algorithmic threshold** separating easy and hard instances

---

## 🧠 Methodology

### k-SAT Representation
- Each instance is defined by:
  - N: number of Boolean variables
  - M: number of clauses
  - K = 3: literals per clause
- Clauses are generated uniformly at random
- The cost function counts the number of unsatisfied clauses

---

### Simulated Annealing Solver

The solver follows a standard Simulated Annealing scheme:
- Random single-variable flips as proposal moves
- Metropolis acceptance rule
- Linear annealing schedule from high to low temperature
- Tracking of acceptance rates and best configurations

Key parameters include:
- Number of Monte Carlo steps per temperature
- Number of annealing steps
- Initial and final inverse temperatures (beta_0, beta_1)

---

## 📊 Performance Analysis

### Single-Instance Behavior
- Acceptance rate evolution illustrates the transition from **exploration** to **exploitation**
- For low clause densities, the solver consistently finds satisfying assignments
- As M increases, the solver increasingly gets trapped in local minima

---

## 📈 Empirical Probability of Solving

For fixed N, the empirical probability

P(N, M) = (number of solved instances) / (total number of instances)

is estimated by averaging over multiple random instances.

### Results
- P(N, M) decreases sharply as the number of clauses M increases
- There exists a critical **algorithmic threshold** M_alg(N) where  
  P(N, M) ≈ 0.5

Below this threshold, Simulated Annealing is likely to find a solution.  
Beyond it, solving the problem becomes increasingly unlikely.

---

## 📉 Scaling and Phase Transition

The analysis is repeated for multiple values of N.

Key observations:
- When plotting P(N, M) as a function of the rescaled ratio M / N,  
  curves for different N approximately collapse
- This indicates that the **clause-to-variable ratio** governs problem hardness

Empirically, the critical ratio is found to be approximately:

**M / N ≈ 3**

This value is lower than the theoretical satisfiability threshold reported in the literature, highlighting the limitations of Simulated Annealing as a heuristic solver for SAT problems.

---

## 📁 Repository Structure

```text
.
├── KSAT.py              # k-SAT problem definition and cost function
├── SimAnn.py            # Generic simulated annealing solver
├── KSATrun.py           # Acceptance-rate analysis for single instances
├── 3SAT_properties.py   # Empirical probability and threshold estimation
├── report.pdf
├── README.md
