# prover generate MQ system and Result V by py/prover.py
```bash
python3 py/prover.py
```
the answer for differnt challenges will be writen in circuits/prover.json
and different ch will also print on the terminal like : 

```bash
    s: [2 2]
    P(s): [76, 56, 46]
    r0,r1 [7 1] [-5  1]
    t0,t1: [5 6] [ 2 -5]
    e0,e1: [1 6 8] [ 64. 211. 214.]
    ans1 [-5, 1] [72, 65, -39]
    ans2 [5, 6] [1, 6, 8]
    ans3 [2, -5] [64, 211, 214]
    ch1 [7, 1] [2, -5] [64, 211, 214]
    ch2 [-5, 1] [2, -5] [64, 211, 214]
    ch3 [-5, 1] [5, 6] [1, 6, 8]
```

```bash
yarn circom:dev --circuit prover
```
this will help you generate commitments by Poseidon Hash

choose the ch you want and get prover_data from challenge.json
```bash
python3 py/verifier.py
```
Automatically help you to copy the commitments and paste to the murphy.json

```bash
yarn circom:dev --circuit murphy
```
Finally, the circuit is finish.
# circom-starter

A basic circom project using [Hardhat](https://github.com/nomiclabs/hardhat) and [hardhat-circom](https://github.com/projectsophon/hardhat-circom). This combines the multiple steps of the [Circom](https://github.com/iden3/circom) and [SnarkJS](https://github.com/iden3/snarkjs) workflow into your [Hardhat](https://hardhat.org) workflow.

By providing configuration containing your Phase 1 Powers of Tau and circuits, this plugin will:

1. Compile the circuits
2. Apply the final beacon
3. Output your `wasm` and `zkey` files
4. Generate and output a `Verifier.sol`

## Documentation

See the source projects for full documentation and configuration

## Install

`yarn` to install dependencies

## Development builds

`yarn circom:dev` to build deterministic development circuits.

Further, for debugging purposes, you may wish to inspect the intermediate files. This is possible with the `--debug` flag which the `circom:dev` task enables by default. You'll find them (by default) in `artifacts/circom/`

To build a single circuit during development, you can use the `--circuit` CLI parameter. For example, if you make a change to `hash.circom` and you want to _only_ rebuild that, you can run `yarn circom:dev --circuit hash`.

## Production builds

`yarn circom:prod` for production builds (using `Date.now()` as entropy)
# pse_hack_circom
