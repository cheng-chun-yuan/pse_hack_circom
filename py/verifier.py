import numpy as np
import json
def get_coefficients():
    read_file = open("coefficient_save.json", "r")
    data = json.load(read_file)
    coefficients = data['coefficients']
    return coefficients

def get_result():
    read_file = open("coefficient_save.json", "r")
    data = json.load(read_file)
    result = data['result']
    return result


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

def get_proof(ch,c1,c2,c3):
    coefficients = get_coefficients()
    result = get_result()
    if ch == 1:
        r = np.array(c1)
        t = np.array(c2)
        e = np.array(c3)
        result1 = r - t
        computed_result = calculate_P(r, coefficients)
        result2 = computed_result - e
        return result1.tolist(), result2.tolist(), t.tolist(), e.tolist()
    if ch == 2:
        result_array = np.array(result)
        r = np.array(c1)
        t = np.array(c2)
        e = np.array(c3)
        f_r = calculate_P(r, coefficients)
        g_t_r = compute_G(t, r, coefficients)
        result2 = result_array - f_r - g_t_r - c3
        return r.tolist(), list(map(int, result2)), t.tolist(), e.tolist()
    if ch == 3:
        r = np.array(c1)
        t = np.array(c2)
        e = np.array(c3)
        g_t_r = compute_G(t, r, coefficients)
        result2 = g_t_r + e
        
        return r.tolist() ,list(map(int, result2)), t.tolist(), e.tolist()
    else:
        return "Invalid choice"

print("proof",get_proof(2 ,[8, 3], [0, -6], [715, 446, 739]))