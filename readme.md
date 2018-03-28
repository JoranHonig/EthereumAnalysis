# Ethereum analysis
This project is meant to perform automatic analysis when smart contracts are created on the ethereum blockchain.

At the moment we only use [mythril](https://github.com/ConsenSys/mythril) as analysis tool but this will be extended in the future
Additionally this now runs as a single instance tool, going forward a more distributed approach might be possible

## Usage
To start an basic setup which uses local only modules and the infura network use the following command:
```
analyzer -l -i
```

## Roadmap
- [ ] Commandline tool
- [ ] Extend Finding to include information like the pc where an error occured, or severity
- [ ] Add [oyente](https://github.com/melonproject/oyente) as an analysis tool
- [ ] Implement a notifier which gets notified by a message broker
- [ ] Report findings to a message broker
- [ ] Implement application which looks for new blocks and notifies a messagebroker
- [ ] Implement application which consumes findings from a message broker and displays/stores the results
