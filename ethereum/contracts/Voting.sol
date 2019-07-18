pragma solidity ^0.4.17;

contract ElectionFactory {
    address[] public elections;

    function createElection() public{
        address election = new Election(msg.sender);
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
    Candidate[] public candidates;

    modifier restricted() {
        require(msg.sender == electionAuthority);
        _;
    }

    function Election(address creator) public {
        electionAuthority = creator;
    }

    function addCandidate(string name, string description) public restricted {
        require(!started);
        Candidate memory candidate = Candidate({
            name: name,
            description: description,
            voteCount: 0
        });
        candidates.push(candidate);
    }

    function commit() public restricted {
        require(!started);
        started = true;
    }

    function finish() public restricted {
        finished = true;
    }

    function vote(uint candidate) public {
        require(!finished);
        require(started);
        require(!voted[msg.sender]);
        voted[msg.sender]=true;
        candidates[candidate].voteCount++;
        voteCount++;
    }
}
