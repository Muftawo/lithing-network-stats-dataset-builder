# *Bitcoin Lightning Network Stats Dataset Builder*
The Bitcoin Lightning Network is a second-layer solution built on top of the Bitcoin blockchain, designed to enable faster and cheaper transactions. It addresses Bitcoin's scalability issues by allowing users to conduct off-chain transactions through payment channels.


# Overview
This is simple poject designed to fetch and sync Bitcoin Lightning Network statistics from Mempool.space public api and stored as a CSV for futher analysis. 

The purpose of this dataset is to capture key metrics that reflect the activity and growth of the Bitcoin Lightning Network over time.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/Muftawo/lithing-network-stats-dataset-builder.git
   cd bitcoin-lightning-stats-builder
   ```

2. Run the main script
   ```bash
   python src/main.py
   ```
3. Monitor the log file:
   You can check the log file for detailed logs.

   ```sh
   tail -f logs/logs.log
   ```


#

## Project Structure

```
lightning_network_stats_dataset_builder/
└───data/
    ├──dataset.csv <- Dataset File
    logs/
    ├──...
    output/
    ├──dataset.csv <- Dataset File
    src/
    ├──...
     test/
    ├──...
    .gitignore
    pyproject.toml
    README.md
```
| Name | Type | Description
| ---- | ---- | -----------
| added | int | The timestamp in milliseconds when the record was added.
| channel_count | int | The total number of channels available.
| total_capacity | int | The total capacity of the network in BTC.
| tor_nodes | int | The total number of nodes running the lightning network over TOR (Anonymous).
| clearnet_nodes | int | The total number of nodes exposing their public IP.
| unannounced_nodes | int | An unannounced node can only be seen by the parties that are involved in the channel.
| clearnet_tor_nodes | int | Nodes running an implementation of Lightning in a dual stack environment making some features public and others private.


#
## Dataset Schema