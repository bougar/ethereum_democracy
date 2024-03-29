const HDWalletProvider = require('truffle-hdwallet-provider');
const Web3 = require('web3');
const compiledFactory = require('./build/ElectionFactory.json')

// Replace with your provider cred
const provider = new HDWalletProvider(
  'test',
  'https://rinkeby.infura.io/v3/da7b9678b9344b2ebaaa8897412a05cd'
);

const web3 = new Web3(provider)

const deploy = async() => {
  const accounts = await web3.eth.getAccounts();
  console.log('Attemping to deploy from account', accounts[0]);

  const result = await new web3.eth.Contract(compiledFactory.abi)
    .deploy({ data: compiledFactory.evm.bytecode.object })
    .send({ gas: '3000000', from: accounts[0] });

  console.log('Contract deployed to',  result.options.address);
}

deploy();
