const assert = require('assert');
const ganache = require('ganache-cli');
const Web3 = require('web3');

const provider = ganache.provider()
provider.setMaxListeners(32);

const web3 = new Web3(provider);

const compiledFactory = require('../ethereum/build/ElectionFactory.json')
const compiledElection = require('../ethereum/build/Election.json')

let accounts;
let factory;
let electionAddress;
let election;

beforeEach(async function() {
  this.timeout(60000);
  accounts = await web3.eth.getAccounts();

  factory = await new web3.eth.Contract(JSON.parse(compiledFactory.interface))
    .deploy({data: '0x' + compiledFactory.bytecode})
    .send({ from: accounts[0], gas: '1000000' });

  await factory.methods.createElection().send({
    from: accounts[0],
    gas: '1000000'
  });

  [electionAddress] = await factory.methods.getElections().call();

  election = await new web3.eth.Contract(
    JSON.parse(compiledElection.interface),
    electionAddress
  );
});


describe('Voting', function() {
  this.timeout(6000);
  it('deploys a factory and a election', () => {
    assert.ok(factory.options.address);
    assert.ok(election.options.address);
  });

  it('electionAuthority address is correctly set', async () => {
    const manager = await election.methods.electionAuthority().call()
    assert.equal(accounts[0], manager)
  });

  it('add Candidate', async () => {
    await election.methods.addCandidate('Alice', 'crypto').send({
      from: accounts[0],
      gas: '1000000'
    });

    const candidate = await election.methods.candidates(0).call();
    assert(candidate.name == 'Alice');
  });

  it('no election manager can add Candidate', async () => {
    try {
      await election.methods.addCandidate('Alice', 'crypto').send({
        from: accounts[1]
      });
      assert(false);
    } catch(err) {
      assert.ok(err);
    }
  });
});
