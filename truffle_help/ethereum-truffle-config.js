 const HDWalletProvider = require('@truffle/hdwallet-provider');
 const mnemonic = ""

module.exports = {

  networks: {
     ropsten: {
       provider: () => new HDWalletProvider(mnemonic, `https://ropsten.infura.io/v3/XXXX`),
       network_id: 3,       // Ropsten's id
       gas: 5500000,        // Ropsten has a lower block limit than mainnet
       confirmations: 2,    // # of confs to wait between deployments. (default: 0)
       timeoutBlocks: 200,
       skipDryRun: true,

        //new
        websockets: true,
        gasPrice: 100000000000,
        networkCheckTimeout: 10000000
     },
  },

  // Set default mocha options here, use special reporters etc.
  mocha: {
    // timeout: 100000
  },

  // Configure your compilers
  compilers: {
    solc: {
       version: "0.7.0",
    }
  }
}
