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

  it('only election manager can add Candidate', async () => {
    try {
      await election.methods.addCandidate('Alice', 'crypto').send({
        from: accounts[1]
      });
      assert(false);
    } catch(err) {
      assert.ok(err);
    }
  });

  it('commit election', async () => {
    await election.methods.commit().send({
      from: accounts[0]
    });
    started = await election.methods.started().call()
    assert(started);
    try {
      await election.methods.commit().send({
        from: accounts[0]
      });
    } catch(err) {
      assert.ok(err)
    }

  });

  it('only manager can commit election', async () => {
    try {
      await election.methods.commit().send({
        from: accounts[1]
      });
      assert(false)
    } catch(err) {
      assert.ok(err)
    }
  });

  it('finish election', async () => {
    await election.methods.commit().send({
      from: accounts[0]
    });
    started = await election.methods.started().call()
    assert(started);

    await election.methods.finish().send({
      from: accounts[0]
    });
    finished = await election.methods.finished().call()
    assert(finished);
    try {
      await election.methods.finish().send({
        from: accounts[0]
      });
    } catch(err) {
      assert.ok(err)
    }
  });

  it('only manager can finish election', async () => {
    await election.methods.commit().send({
      from: accounts[0]
    });
    try {
      await election.methods.finish().send({
        from: accounts[1]
      });
      assert(false)
    } catch(err) {
      assert.ok(err)
    }
  });

  it('vote to a candidate', async () => {
    await election.methods.addCandidate('Bob', 'Description').send({
      from: accounts[0],
      gas: '1000000'
    });
    await election.methods.commit().send({
      from: accounts[0]
    });
    started = await election.methods.started().call()
    assert(started);
    await election.methods.vote(0).send({
      from: accounts[1]
    });
    const candidate = await election.methods.candidates(0).call();
    assert(candidate.voteCount == 1);
  });

  it('cannot vote more than once', async () => {
    await election.methods.addCandidate('Bob', 'Description').send({
      from: accounts[0],
      gas: '1000000'
    });
    await election.methods.commit().send({
      from: accounts[0]
    });
    started = await election.methods.started().call()
    assert(started);
    await election.methods.vote(0).send({
      from: accounts[1]
    });
    const candidate = await election.methods.candidates(0).call();
    assert(candidate.voteCount == 1);
    try {
      await election.methods.vote(0).send({
        from: accounts[1]
      });
    } catch (err) {
      assert(err)
    }
  });

  it('cannot vote when finished', async () => {
    await election.methods.addCandidate('Bob', 'Description').send({
      from: accounts[0],
      gas: '1000000'
    });
    await election.methods.commit().send({
      from: accounts[0]
    });
    started = await election.methods.started().call()
    assert(started);
    await election.methods.finish().send({
      from: accounts[0]
    });
    finished = await election.methods.finished().call()
    assert(finished)
    try {
      await election.methods.vote(0).send({
        from: accounts[1]
      });
    } catch (err) {
      assert(err)
    }
  });
});

