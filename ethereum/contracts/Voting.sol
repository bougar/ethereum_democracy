pragma solidity ^0.4.17;

contract ElectionFactory {
    address[] public elections;

    function createElection(string name, string description) public{
        address election = new Election(msg.sender, name, description);
        elections.push(election);
    }

    function getElections() public view returns (address[]) {
        return elections;
    }
}

contract Election {
    struct Candidate {
        string name;
        string description;
        uint voteCount;
    }

    bool public started = false;
    bool public finished = false;
    address public electionAuthority;
    mapping(address => bool) public voted;
    uint public voteCount;
    uint public initTime;
    uint public finalTime;
    string public name;
    string public description;
    Candidate[] public candidates;

    modifier restricted() {
        require(msg.sender == electionAuthority);
        _;
    }

    modifier onTime() {
        require(now > initTime);
        if (finalTime != 0) {
            require (now < finalTime);
        }
        _;
    }

    function Election(address creator, string _name, string _description) public {
        name = _name;
        description = _description;
        electionAuthority = creator;
        initTime = 0;
        finalTime = 0;
    }


    function addCandidate(string _name, string _description) public restricted {
        require(!started);
        Candidate memory candidate = Candidate({
            name: _name,
            description: _description,
            voteCount: 0
        });
        candidates.push(candidate);
    }

    function setPeriod(uint _initTime, uint _finalTime) public restricted {
        require(!started);
        if (_initTime != 0) {
            require(_initTime > (now - 900));
        }
        if (_finalTime != 0) {
            require(_finalTime > (now - 900));
        }
        if (_finalTime != 0 && _initTime != 0) {
            require (_finalTime - _initTime >= 3600);
        }
        initTime = _initTime;
        finalTime = _finalTime;
    }

    function commit() public restricted {
        require(!started);
        started = true;
    }

    function finish() public restricted {
        require(started);
        require(!finished);
        finished = true;
    }

    function vote(uint candidate) public onTime {
        require(started);
        require(!finished);
        require(!voted[msg.sender]);
        voted[msg.sender]=true;
        candidates[candidate].voteCount++;
        voteCount++;
    }
}
