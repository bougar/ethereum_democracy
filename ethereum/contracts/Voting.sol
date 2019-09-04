pragma solidity ^0.5.11;

contract ElectionFactory {
    mapping(address => bool) public electionExist;
    mapping(string => address) public electionNames;
    address[] public elections;

    function createElection(string memory name) public {
        require(bytes(name).length > 0);
        require(electionNames[name] == address(0));
        address election = address(new Election(msg.sender, name));
        electionExist[election] = true;
        electionNames[name] = election;
        elections.push(election);
    }

    function getElections() public view returns (address[] memory) {
        return elections;
    }
}

contract Election {
    struct Candidate {
        string name;
        uint voteCount;
    }

    bool public commited = false;
    bool public finished = false;
    address public electionAuthority;
    mapping(address => bool) public voted;
    uint public voteCount;
    uint public initTime;
    uint public finalTime;
    string public name;
    Candidate[] public candidates;
    uint public numCandidates;

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

    constructor(address creator, string memory _name) public {
        name = _name;
        electionAuthority = creator;
        initTime = 0;
        finalTime = 0;
    }


    function addCandidate(string memory _name) public restricted {
        require(!commited);
        Candidate memory candidate = Candidate({
            name: _name,
            voteCount: 0
        });
        numCandidates ++;
        candidates.push(candidate);
    }


    function setPeriod(uint _initTime, uint _finalTime) public restricted {
        require(!commited);
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
        require(!commited);
        commited = true;
    }

    function finish() public restricted {
        require(commited);
        require(!finished);
        finished = true;
    }

    function vote(uint candidate) public onTime {
        require(commited);
        require(!finished);
        require(!voted[msg.sender]);
        voted[msg.sender]=true;
        candidates[candidate].voteCount++;
        voteCount++;
    }
}
