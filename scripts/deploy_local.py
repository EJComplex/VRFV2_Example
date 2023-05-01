# Copy the following Contracts
#
# LinkToken
# MockV3Aggregator
# VRFCoordinatorV2Mock
# VRFV2Wrapper
#
# Example Local Implementation
# RandomNumberDirectFundingConsumerV2


from scripts.helpful_scripts import get_account
from brownie import (
    accounts,
    MockV3Aggregator,
    RandomNumberDirectFundingConsumerV2,
    VRFCoordinatorV2Mock,
    VRFV2Wrapper,
    LinkToken,
)
from brownie.network.gas.strategies import GasNowStrategy
from eth_abi import encode_abi

import time
from web3 import Web3


def main():
    account = accounts[0]

    # deploy VRFCoordinatorV2Mock
    VRFCoordinatorV2Mock_Deployed = VRFCoordinatorV2Mock.deploy(
        100000000000000000,
        1000000000,
        {"from": account},
    )

    # deploy MockV3Aggregator
    MockV3Aggregator_Deployed = MockV3Aggregator.deploy(
        18,
        3000000000000000,
        {"from": account},
    )

    # deploy LinkToken
    LinkToken_Deployed = LinkToken.deploy(
        {"from": account},
    )

    # deploy VRFV2Wrapper
    VRFV2Wrapper_Deployed = VRFV2Wrapper.deploy(
        LinkToken_Deployed.address,
        MockV3Aggregator_Deployed.address,
        VRFCoordinatorV2Mock_Deployed.address,
        {"from": account},
    )

    # Set V2Wrapper Config
    tx_config = VRFV2Wrapper_Deployed.setConfig(
        60000,
        52000,
        10,
        "0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc",
        10,
        {"from": account},
    )

    # Fund VRFV2Wrapper
    tx_fund = VRFCoordinatorV2Mock_Deployed.fundSubscription(
        1, 10000000000000000000, {"from": account}
    )

    # deploy VRFConsumer
    RandomNumberDirectFundingConsumerV2_Deployed = (
        RandomNumberDirectFundingConsumerV2.deploy(
            LinkToken_Deployed.address,
            VRFV2Wrapper_Deployed.address,
            {"from": account},
        )
    )

    tx_fund_link = LinkToken_Deployed.transfer(
        RandomNumberDirectFundingConsumerV2_Deployed.address,
        100000000000000000000,
        {"from": account},
    )

    tx_request_random_words = (
        RandomNumberDirectFundingConsumerV2_Deployed.requestRandomWords(
            300000, 3, 3, {"from": account}
        )
    )

    # print(tx_request_random_words.events["RequestSent"]["requestId"])

    # Fulfill Request
    tx_fulfill = VRFCoordinatorV2Mock_Deployed.fulfillRandomWords(
        tx_request_random_words.events["RequestSent"]["requestId"],
        VRFV2Wrapper_Deployed,
        {"from": account},
    )

    # print random words
    print(tx_fulfill.events["RequestFulfilled"]["randomWords"])

    time.sleep(5)

    # abi.encode(_callbackGasLimit, _requestConfirmations, _numWords)
    # print(
    #     LinkToken_Deployed.balanceOf(
    #         RandomNumberDirectFundingConsumerV2_Deployed.address, {"from": account}
    #     )
    # )

    # tx = VRFV2Wrapper_Deployed.calculateRequestPrice(300000, {"from": account})

    # print(tx)

    # tx_encode = LinkToken_Deployed.transferAndCall(
    #     VRFV2Wrapper_Deployed.address,
    #     tx,
    #     encode_abi(["uint32", "uint16", "uint32"], [300000, 3, 3]),
    # )
