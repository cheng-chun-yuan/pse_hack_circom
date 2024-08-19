import numpy as np
import json

def initialize_coefficients(m, n, low=0):
    """Initialize coefficients for the quadratic system."""
    p_ij = np.random.randint(0, 10, size=(m, n, n))  # Coefficients for x_i * x_j
    p_i = np.random.randint(0, 10, size=(m, n))      # Coefficients for x_i
    p_0 = np.zeros(m)                               # Constant coefficients
    return {'p_ij': p_ij.tolist(), 'p_i': p_i.tolist(), 'p_0': p_0.tolist()}

def calculate_P(x, coefficients):
    """Calculate P(x) using the provided coefficients."""
    p_ij = coefficients['p_ij']
    p_i = coefficients['p_i']
    p_0 = coefficients['p_0']

    # Calculate the quadratic term
    quadratic_term = np.einsum('kij,i,j->k', p_ij, x, x)
    
    # Calculate the linear term
    linear_term = np.dot(p_i, x)
    
    # Combine the terms
    P = quadratic_term + linear_term + p_0
    
    return P

def compute_G(r0, r1, coefficients):
    """Compute G(r0, r1) based on the provided coefficients."""
    P_r0_plus_r1 = calculate_P(r0 + r1, coefficients)
    P_r0 = calculate_P(r0, coefficients)
    P_r1 = calculate_P(r1, coefficients)
    P_0 = calculate_P(np.zeros_like(r0), coefficients)

    G = P_r0_plus_r1 - P_r0 - P_r1 + P_0
    return G

# Example usage
m = 3 
n = 2 

# Initialize coefficients, Generate MQ system
coefficients = initialize_coefficients(m, n)

# Example input vector s (randomly generated or you can specify your own)
s = np.random.randint(0, 10, size=n)
print("s:", s)

# Calculate P(s)
result_v = calculate_P(s, coefficients)
print("P(s):", result_v)
#also write the result_v to file_path

# result_v and MQ system coefficients are public and can be shared with the verifier
file_path = 'coefficient.json'  # Specify the file name
data_to_save = {
    'result_v': result_v.tolist(),
    'coefficients': coefficients
}
with open(file_path, 'w') as f:
    json.dump(data_to_save, f, indent=4)

print(f"Coefficients and result_v saved to {file_path}")

#Separate the x randomly to get r0 and r1
r0 = np.random.randint(0, 10, size=n)
r1 = s - r0

#Separate the r0 randomly to get t0 and t1 
t0 = np.random.randint(0, 10, size=n)
t1 = r0 - t0

#Compute P(r0) and separate the r0 randomly to get e0 and e1
P_r0 = calculate_P(r0, coefficients)
e0 = np.random.randint(0, 10, size=m)
e1 = P_r0 - e0

print("r0:", r0)
print("r1:", r1)
print("t0:", t0)
print("t1:", t1)
print("e0:", e0)
print("e1:", e1)
print("ans1", list(map(int, r1)), list(map(int, compute_G(t1, r1, coefficients))))
print("ans2", list(map(int, t0)), list(map(int, e0)))
print("ans3", list(map(int, t1)), list(map(int, e1)))

print("ch1", 1, r0.tolist(), t1.tolist(), list(map(int, e1)))
print("ch2", 2, r1.tolist(), t1.tolist(), list(map(int, e1)))
print("ch3", 3, r1.tolist(), t0.tolist(), list(map(int, e0)))
