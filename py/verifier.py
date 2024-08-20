import numpy as np
import json
def get_coefficients():
    read_file = open("coefficient.json", "r")
    data = json.load(read_file)
    coefficients = data['coefficients']
    return coefficients

def get_result():
    read_file = open("coefficient.json", "r")
    data = json.load(read_file)
    result = data['result_v']
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

def update_json_values(target_json_path,value):
    # Read the prover.public.json file
    with open(target_json_path, 'r') as f:
        target_json = json.load(f)

    # Update the target JSON object with new c1, c2, c3 values
    target_json['ch'] = value[0]
    target_json['a'] = value[1]
    target_json['b'] = value[2]
    target_json['c'] = value[3]
    target_json['d'] = value[4]

    # Save the updated JSON back to the target file (murphy.json)
    with open(target_json_path, 'w') as f:
        json.dump(target_json, f, indent=2)

    return target_json

def update_choice_values(public_json_path, target_json_path):
    # Read the prover.public.json file
    with open(public_json_path, 'r') as f:
        prover_data = json.load(f)
    
    # Extract the required values from prover.public.json
    c_values = prover_data[:3]  # Assuming the first three values correspond to c1, c2, c3

    # Read the target murphy.json file
    with open(target_json_path, 'r') as f:
        target_json = json.load(f)

    # Update the target JSON object with new c1, c2, c3 values
    target_json['c1'] = c_values[0]
    target_json['c2'] = c_values[1]
    target_json['c3'] = c_values[2]

    # Save the updated JSON back to the target file (murphy.json)
    with open(target_json_path, 'w') as f:
        json.dump(target_json, f, indent=2)

    return target_json


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
        update_json_values('circuits/murphy.json',[0, result1.tolist(), result2.tolist(), t.tolist(), e.tolist()])
        return result1.tolist(), list(map(int, result2)), t.tolist(), e.tolist()
    if ch == 2:
        result_array = np.array(result)
        r = np.array(c1)
        t = np.array(c2)
        e = np.array(c3)
        f_r = calculate_P(r, coefficients)
        g_t_r = compute_G(t, r, coefficients)
        result2 = result_array - f_r - g_t_r - c3
        update_json_values('circuits/murphy.json',[1, r.tolist(), list(map(int, result2)), t.tolist(), e.tolist()])
        return r.tolist(), list(map(int, result2)), t.tolist(), e.tolist()
    if ch == 3:
        r = np.array(c1)
        t = np.array(c2)
        e = np.array(c3)
        g_t_r = compute_G(t, r, coefficients)
        result2 = g_t_r + e
        update_json_values('circuits/murphy.json',[2, r.tolist() ,list(map(int, result2)), t.tolist(), e.tolist()])
        return r.tolist() ,list(map(int, result2)), t.tolist(), e.tolist()
    else:
        return "Invalid choice"

# Example usage:
public_json_path = 'artifacts/circom/prover.public.json'
target_json_path = 'circuits/murphy.json'

# Update the target murphy.json
updated_json = update_choice_values(public_json_path, target_json_path)


choice=0
while choice==0:
    print ("""
    1.Challenge 1
    2.Challenge 2
    3.Challenge 3
    """)
    choice=input("Whic would you like? ") 

# Get the prover data from challenges.json according to the choice
with open('challenges.json', 'r') as f:
    prover_data = json.load(f)[f'ch{choice}']
print("proof",get_proof(*prover_data))