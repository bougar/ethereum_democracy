import election
import json
from web3 import HTTPProvider

def main():
    account = '0xebad0c65fd9879d6d5b7a20a5cce221034b41bee'
    pkey = '0xE2506B36576DC029AF8EE08E3C2A2352A1B63C1433322BA4A5485778C6B42D98'.lower()
    provider = HTTPProvider('https://rinkeby.infura.io/v3/da7b9678b9344b2ebaaa8897412a05cd')
    address = '0x6aa21514273630de677b9cbc6ce538db2e75cece'

    with open('/home/bougar/Documents/voting/ethereum/build/ElectionFactory.json') as js:
        inter = json.loads(js.read())['interface']
    contract = election.Ethereum(provider, address, inter)
    return contract.send('createElection', account, pkey, ['hola', 'mundo'], {
        'gas': 300000
    })

main()
