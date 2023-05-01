# Example Sepolia testnet implementation
# VRFv2DirectFundngConsumer


from scripts.helpful_scripts import get_account
from brownie import (
    VRFv2DirectFundingConsumer,
    network,
    config,
    accounts,
    interface,
    Contract,
)
from brownie.network.gas.strategies import GasNowStrategy


import time
from web3 import Web3


def main():
    account = accounts.add(config["wallets"]["from_key"])

    deployedContract = VRFv2DirectFundingConsumer.deploy(
        {"from": account},
        publish_source=True,
    )

    # gas_strategy = GasNowStrategy("fast")

    # deployedContract = Contract.from_abi(
    #     VRFv2DirectFundingConsumer._name,
    #     "0x57ff19a28c3bcC678DEDb675E78DFDe39454c05E",
    #     VRFv2DirectFundingConsumer.abi,
    # )

    LINK_ADDRESS = "0x779877A7B0D9E8603169DdbD7836e478b4624789"

    LINK = interface.LinkTokenInterface(LINK_ADDRESS)

    tx_fund = LINK.transfer(
        deployedContract.address,
        Web3.toWei(2, "ether"),
        {"from": account, "priority_fee": "20 gwei"},
    )

    tx_fund.wait(10)

    tx_random = deployedContract.requestRandomWords(
        {
            "from": account,
            "priority_fee": "20 gwei",
        }
    )

    tx_random.wait(1)
