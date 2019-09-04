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

  factory = await new web3.eth.Contract(compiledFactory.abi)
    .deploy({data: '0x' + compiledFactory.evm.bytecode.object})
    .send({ from: accounts[0], gas: '3000000' });

  await factory.methods.createElection('test').send({
    from: accounts[0],
    gas: '1000000'
  });

  [electionAddress] = await factory.methods.getElections().call();

  election = await new web3.eth.Contract(
    compiledElection.abi,
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
    await election.methods.addCandidate('Alice').send({
      from: accounts[0],
      gas: '1000000'
    });

    const candidate = await election.methods.candidates(0).call();
    assert(candidate.name == 'Alice');
  });

  it('only election manager can add Candidate', async () => {
    try {
      await election.methods.addCandidate('Alice').send({
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
    commited = await election.methods.commited().call()
    assert(commited);
    try {
      await election.methods.commit().send({
        from: accounts[0]
      });
      assert(false)
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
    commited = await election.methods.commited().call()
    assert(commited);

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
    await election.methods.addCandidate('Bob').send({
      from: accounts[0],
      gas: '1000000'
    });
    await election.methods.commit().send({
      from: accounts[0]
    });
    commited = await election.methods.commited().call()
    assert(commited);
    await election.methods.vote(0).send({
      from: accounts[1]
    });
    const candidate = await election.methods.candidates(0).call();
    assert(candidate.voteCount == 1);
  });

  it('cannot vote more than once', async () => {
    await election.methods.addCandidate('Bob').send({
      from: accounts[0],
      gas: '1000000'
    });
    await election.methods.commit().send({
      from: accounts[0]
    });
    commited = await election.methods.commited().call()
    assert(commited);
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
  it('can set time period', async () => {
    init = Date.now()
    finish = init + 3600
    await election.methods.setPeriod(init, finish).send({
      from: accounts[0],
      gas: '1000000'
    })
    contract_init = await election.methods.initTime().call();
    contract_finish = await election.methods.finalTime().call();
    assert(init == contract_init);
    assert(finish == contract_finish);
  });
  it('only master can set time period', async () => {
    try {
      await election.methods.setPeriod(init, finish).send({
        from: accounts[1],
        gas: '1000000'
      })
      assert(false);
    } catch(err){
      assert(err);
    }
  });
  it('cannot set time period when commited', async() => {
    await election.methods.commit().send({
      from: accounts[0],
      gas: '1000000'
    })
    try {
      await election.methods.setPeriod(init, finish).send({
        from: accounts[0],
        gas: '1000000'
      })
      assert(false);
    } catch(err){
      assert(err);
    }
  });
  it('cannot set time period lower than one hour', async() => {
    init = Date.now()
    finish = init + 3599
    try {
      await election.methods.setPeriod(init, finish).send({
        from: accounts[0],
        gas: '1000000'
      })
      assert(false);
    } catch(err){
      assert(err);
    }
  });
  it('cannot set init time period lower than now (take into account eth tolerance)', async() => {
    init = Date.now() - 901
    finish = init + 3600
    try {
      await election.methods.setPeriod(init, finish).send({
        from: accounts[0],
        gas: '1000000'
      })
      assert(false);
    } catch(err){
      assert(err);
    }
  });
  it('can set only init time', async () => {
    init = Date.now()
    finish = 0
    await election.methods.setPeriod(init, finish).send({
      from: accounts[0],
      gas: '1000000'
    })
    contract_init = await election.methods.initTime().call();
    contract_finish = await election.methods.finalTime().call();
    assert(init == contract_init);
    assert(finish == contract_finish);
  });
  it('can set only final time', async () => {
    init = 0
    finish = Date.now() + 3600
    await election.methods.setPeriod(init, finish).send({
      from: accounts[0],
      gas: '1000000'
    })
    contract_init = await election.methods.initTime().call();
    contract_finish = await election.methods.finalTime().call();
    assert(init == contract_init);
    assert(finish == contract_finish);
  });
  it('cannot vote when finished', async () => {
    await election.methods.addCandidate('Bob').send({
      from: accounts[0],
      gas: '1000000'
    });
    await election.methods.commit().send({
      from: accounts[0]
    });
    commited = await election.methods.commited().call()
    assert(commited);
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

