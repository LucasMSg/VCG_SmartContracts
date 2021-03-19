How to use:

it is necessary to install truffle
https://www.trufflesuite.com/docs/truffle/getting-started/installation
https://www.trufflesuite.com/docs/tezos/truffle/quickstart

Setup for Ethereum:
1. Create a wallet with Metamask.
2. Get testnet Eth form a faucet, example: https://faucet.dimensions.network/.
3. Create an Ethereum project on Infura https://infura.io/
4. On settings, select Ropsten and copy the http entrypoint.
5. Install HDWalletProvider "npm install @truffle/hdwallet-provider"
6. Truffle set up:
  -Create a new directory for your Truffle project
  -Create a bare Truffle projecte "truffle init"
  -Copy the vcg.sol contract into the contracts folder
  -In the folder migrations, create a migration file for vcg, see the example in the folder truffle_help
  -configure truffle-config with HDWalletProvider, your mnemonics and your infura project's entrypoint. And the Ropsten network. See the example in the folder truffle_help.


Setup for Tezos,
1. Get a faucet wallet https://faucet.tzalpha.net/
2. Configure the truffle-config file with mnemonic, secret, password and  email from the faucet file as well as configure the development network, we used delphinet.See the example in the folder truffle_help.
3. Truffle set up:
  -Create a new directory for your Truffle project
  -Create a bare Truffle projecte "truffle init"
  -Copy the vcg.tz contract into the contracts folder (This is the michelson code compiled from vcg.py)
  -In the folder migrations, create a migration file for vcg, see the example in the folder truffle_help
  -configure truffle-config with mnemonic, secret, password and  email from the faucet file as well as configure the delphinet development network.



Tests:
Execute the python script with a number of bids and the ctrs as per the following example:
python3 test.py 10 4,3,2,1
It will then generate the javascript files for truffle exec.

Ethereum:
1. Fist deploy a new contract.
truffle migrate --network ropsten --reset
2. Execute test.
truffle exec ./scriptE.js --network ropsten

Tezos:
1. Fist deploy a new contract.
time truffle migrate --reset
2. Execute test.
truffle exec ./scriptT.js
