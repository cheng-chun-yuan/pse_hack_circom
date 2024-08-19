pragma circom 2.1.4;

include "../node_modules/circomlib/circuits/poseidon.circom";
include "../node_modules/circomlib/circuits/comparators.circom";

template get_commitment(n, m) {
  signal input a1[n];
  signal input b1[m];
  signal input a2[n];
  signal input b2[m];
  signal input a3[n];
  signal input b3[m];
  signal output hash1;
  signal output hash2;
  signal output hash3; 

  component hashed1 = Poseidon(n+m);
  component hashed2 = Poseidon(n+m);
  component hashed3 = Poseidon(n+m);
  // First Hash Calculation
  for (var i = 0; i < n; i++) {
    hashed1.inputs[i] <== a1[i];
    hashed2.inputs[i] <== a2[i];
    hashed3.inputs[i] <== a3[i];
  }
  for (var i = 0; i < m; i++) {
    hashed1.inputs[n+i] <== b1[i];
    hashed2.inputs[n+i] <== b2[i];
    hashed3.inputs[n+i] <== b3[i];
  }
  hash1 <== hashed1.out;
  hash2 <== hashed2.out;
  hash3 <== hashed3.out;

}

component main = get_commitment(2, 3);
