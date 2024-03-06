"""
Interact with the intelchain blockchain to fetch
blocks, headers, transaction pool, node status, etc.
"""
# pylint: disable=too-many-lines
from .rpc.request import rpc_request

from .exceptions import InvalidRPCReplyError

from .constants import DEFAULT_ENDPOINT, DEFAULT_TIMEOUT


#############################
# Node / network level RPCs #
#############################
def get_bad_blocks(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> list:
    """[WIP] Get list of bad blocks in memory of specific node Known issues
    with RPC not returning correctly.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of bad blocks in node memory

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#0ba3c7b6-6aa9-46b8-9c84-f8782e935951
    """
    method = "itcv2_getCurrentBadBlocks"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def chain_id( endpoint = DEFAULT_ENDPOINT, timeout = DEFAULT_TIMEOUT ) -> dict:
    """Chain id of the chain.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int that represents the chain id

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/343dbe89b3c105f8104ab877769070ba6fdd0133/rpc/blockchain.go#L44
    """
    method = "itcv2_chainId"
    try:
        data = rpc_request( method, endpoint = endpoint, timeout = timeout )
        return data[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_node_metadata(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> dict:
    """Get config for the node.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict with the following keys:
        blskey: :obj:`list` of BLS keys on the node
        version: :obj:`str` representing the intelchain binary version
        network: :obj:`str` the Network name that the node is on (Mainnet or Testnet)
        chain-config: :obj:`dict` with the hard fork epochs list, and `chain-id`
            both as :obj:`int`
        is-leader: :obj:`bool` Whether the node is currently leader or not
        shard-id: :obj:`int` Shard that the node is on
        current-epoch: :obj:`int` Current epoch
        blocks-per-epoch: :obj:`int` Number of blocks per epoch (only available on Shard 0)
        role: :obj:`str` Node type(Validator or ExplorerNode)
        dns-zone: :obj:`str`: Name of the DNS zone
        is-archival: :obj:`bool` Whether the node is currently in state pruning mode or not
        node-unix-start-time: :obj:`int` Start time of node un Unix time
        p2p-connectivity: :obj:`dict` with the following keys:
            connected: :obj:`int` Number of connected peers
            not-connected: :obj:`int` Number of peers which are known but not connected
            total-known-peers: :obj:`int` Number of peers which are known
        peerid: :obj:`str` PeerID, the pubkey for communication
        consensus: :obj:`dict` with following keys:
            blocknum: :obj:`int` Current block number of the consensus
            finality: :obj:`int` The finality time in milliseconds of previous consensus
            mode: :obj:`str` Current consensus mode
            phase: :obj:`str` Current consensus phase
            viewChangeId: :obj:`int` Current view changing ID
            viewId: :obj:`int` Current view ID
        sync-peers: dictionary of connected sync peers for each shard

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#03c39b56-8dfc-48ce-bdad-f85776dd8aec
    https://github.com/zennittians/intelchain/blob/v1.10.2/internal/params/config.go#L233
    https://github.com/zennittians/intelchain/blob/9f320436ff30d9babd957bc5f2e15a1818c86584/node/api.go#L110
    """
    method = "itcv2_getNodeMetadata"
    try:
        metadata = rpc_request( method, endpoint = endpoint, timeout = timeout )
        return metadata[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_peer_info(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> dict:
    """Get peer info for the node.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    if has peers, dict with the following keys:
        blocked-peers: :obj:`list` list of blocked peers by peer ID
        connected-peers: :obj:`list` list of connected peers by topic
            peers: :obj:`list` list of connected peer IDs
            topic: :obj:`list` topic of the connection, for example:
                'intelchain/0.0.1/client/beacon'
                'intelchain/0.0.1/node/beacon'
        peerid: :obj:`str` Peer ID of the node

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    See also
    --------
    get_node_metadata
    """
    method = "itcv2_getPeerInfo"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def protocol_version(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get the current intelchain protocol version this node supports.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        The current intelchain protocol version this node supports

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#cab9fcc2-e3cd-4bc9-b62a-13e4e046e2fd
    """
    method = "itcv2_protocolVersion"
    try:
        value = rpc_request( method, endpoint = endpoint, timeout = timeout )
        return value[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_num_peers(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get number of peers connected to the node.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of connected peers

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#09287e0b-5b61-4d18-a0f1-3afcfc3369c1
    """
    method = "net_peerCount"
    try:  # Number of peers represented as a hex string
        return int(
            rpc_request( method,
                         endpoint = endpoint,
                         timeout = timeout )[ "result" ],
            16
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_version(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get version of the EVM network (https://chainid.network/)

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Version if the network

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#09287e0b-5b61-4d18-a0f1-3afcfc3369c1
    """
    method = "net_version"
    try:
        return int(
            rpc_request( method,
                         endpoint = endpoint,
                         timeout = timeout )[ "result" ],
            16
        )  # this is hexadecimal
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def in_sync( endpoint = DEFAULT_ENDPOINT, timeout = DEFAULT_TIMEOUT ) -> bool:
    """Whether the shard chain is in sync or syncing (not out of sync)

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    bool, True if in sync

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/blockchain.go#L690
    """
    method = "itcv2_inSync"
    try:
        return bool(
            rpc_request( method,
                         endpoint = endpoint,
                         timeout = timeout )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def beacon_in_sync(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> bool:
    """Whether the beacon chain is in sync or syncing (not out of sync)

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    bool, True if sync

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/blockchain.go#L695
    """
    method = "itcv2_beaconInSync"
    try:
        return bool(
            rpc_request( method,
                         endpoint = endpoint,
                         timeout = timeout )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_staking_epoch(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get epoch number when blockchain switches to EPoS election.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Epoch at which blockchain switches to EPoS election

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    ---------
    https://github.com/zennittians/intelchain/blob/v1.10.2/internal/params/config.go#L233

    See also
    ------
    get_node_metadata
    """
    method = "itcv2_getNodeMetadata"
    try:
        data = rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
        return int( data[ "chain-config" ][ "staking-epoch" ] )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_prestaking_epoch(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get epoch number when blockchain switches to allow staking features
    without election.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Epoch at which blockchain switches to allow staking features without election

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/v1.10.2/internal/params/config.go#L233

    See also
    ------
    get_node_metadata
    """
    method = "itcv2_getNodeMetadata"
    try:
        data = rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
        return int( data[ "chain-config" ][ "prestaking-epoch" ] )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


########################
# Sharding information #
########################
def get_shard( endpoint = DEFAULT_ENDPOINT, timeout = DEFAULT_TIMEOUT ) -> int:
    """Get shard ID of the node.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Shard ID of node

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    See also
    --------
    get_node_metadata
    """
    method = "itcv2_getNodeMetadata"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ][ "shard-id" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_sharding_structure(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> list:
    """Get network sharding structure.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of dictionaries of shards; each shard has the following keys
    shardID: :obj:`int` ID of the shard
    current: :obj:`bool` True if the endpoint passed is the same shard as this one
    http: :obj:`str` Link to the HTTP(s) API endpoint
    wss: :obj:`str` Link to the Web socket endpoint

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#9669d49e-43c1-47d9-a3fd-e7786e5879df
    """
    method = "itcv2_getShardingStructure"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


#############################
# Current status of network #
#############################
def get_leader_address(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> str:
    """Get current leader one address.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        One address of current leader

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#8b08d18c-017b-4b44-a3c3-356f9c12dacd
    """
    method = "itcv2_getLeader"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def is_last_block(
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> bool:
    """If the block at block_num is the last block.

    Parameters
    ----------
    block_num: :obj:`int`
        Block number to fetch
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    bool: True if the block is last epoch block, False otherwise

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/blockchain.go#L286
    """
    params = [ block_num, ]
    method = "itcv2_isLastBlock"
    try:
        return bool(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def epoch_last_block(
    epoch,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Returns the number of the last block in the epoch.

    Parameters
    ----------
    epoch: :obj:`int`
        Epoch for which the last block is to be fetched
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int: Number of the last block in the epoch

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/blockchain.go#L294
    """
    params = [ epoch, ]
    method = "itcv2_epochLastBlock"
    try:
        return int(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_circulating_supply(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get current circulation supply of tokens in ONE.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Current circulation supply (with decimal point)

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#8398e818-ac2d-4ad8-a3b4-a00927395044
    """
    method = "itcv2_getCirculatingSupply"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_total_supply(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get total number of pre-mined tokens.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    str
        Total number of pre-mined tokens, or None if no such tokens

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#3dcea518-9e9a-4a20-84f4-c7a0817b2196
    """
    method = "itcv2_getTotalSupply"
    try:
        rpc_request( method,
                     endpoint = endpoint,
                     timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_number(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get current block number.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Current block number

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#2602b6c4-a579-4b7c-bce8-85331e0db1a7
    """
    method = "itcv2_blockNumber"
    try:
        return int(
            rpc_request( method,
                         endpoint = endpoint,
                         timeout = timeout )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_current_epoch(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get current epoch number.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Current epoch number

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#9b8e98b0-46d1-4fa0-aaa6-317ff1ddba59
    """
    method = "itcv2_getEpoch"
    try:
        return int(
            rpc_request( method,
                         endpoint = endpoint,
                         timeout = timeout )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_last_cross_links(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> list:
    """Get last cross shard links.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of dictionaries, one for each shard except the one at the endpoint; each representing
    the last block on the beacon-chain
        hash: :obj:`str` Parent block hash
        block-number: :obj:`int` Block number
        view-id: :obj:`int` View ID
        signature: :obj:`str` Hex representation of aggregated signature
        signature-bitmap: :obj:`str` Hex representation of aggregated signature bitmap
        shard-id: :obj:`str` (other) shard ID
        epoch-number: :obj:`int` Block epoch

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#4994cdf9-38c4-4b1d-90a8-290ddaa3040e
    """
    method = "itcv2_getLastCrossLinks"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_gas_price(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get network gas price.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Network gas price

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#1d53fd59-a89f-436c-a171-aec9d9623f48
    """
    method = "itcv2_gasPrice"
    try:
        return int(
            rpc_request( method,
                         endpoint = endpoint,
                         timeout = timeout )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


##############
# Block RPCs #
##############
def get_latest_header(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> dict:
    """Get block header of latest block.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict with the following keys:
        blockHash: :obj:`str` Block hash
        blockNumber: :obj:`int` Block number
        shardID: :obj:`int` Shard ID
        leader: :obj:`str` Wallet address of leader that proposed this block if prestaking
            otherwise sha256 hash of leader's public bls key
        viewID: :obj:`int` View ID of the block
        epoch: :obj:`int` Epoch of block
        timestamp: :obj:`str` Timestamp that the block was finalized in human readable format
        unixtime: :obj:`int` Timestamp that the block was finalized in Unix time
        lastCommitSig: :obj:`str` Hex representation of aggregated signatures of the previous block
        lastCommitBitmap: :obj:`str`
            Hex representation of aggregated signature bitmap of the previous block
        crossLinks:list of dicts describing the cross shard links:
            block-number: :obj:`int` Number of the cross link block
            epoch-number: :obj:`int` Epoch of the cross link block
            hash: :obj:`str` Hash of the cross link block
            shard-id: :obj:`int` Shard ID for the cross link (besides the shard at endpoint)
            signature: :obj:`str` Aggregated signature of the cross link block
            siganture-bitmap: :obj:`str` Aggregated signature bitmap of the cross link block
            view-id: :obj:`int` View ID of the cross link block
    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#73fc9b97-b048-4b85-8a93-4d2bf1da54a6
    """
    method = "itcv2_latestHeader"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_header_by_number(
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> dict:
    """Get block header of block at block_num.

    Parameters
    ----------
    block_num: :obj:`int`
        Number of the block whose header is requested
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    See get_latest_header for header structure

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#01148e4f-72bb-426d-a123-718a161eaec0
    """
    method = "itcv2_getHeaderByNumber"
    params = [ block_num ]
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_latest_chain_headers(
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> dict:
    """Get block header of latest block for beacon chain & shard chain.

    Parameters
    ----------
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict with two keys:
        beacon-chain-header: :obj:`dict` with the following keys, applicable to the beacon chain
        shard-chain-header: :obj:`dict` with the following keys, applicable to the shard chain
            difficulty: legacy
            epoch: :obj:`int` Epoch of the block
            extraData: legacy
            gasLimit: legacy
            gasUsed: legacy
            hash: :obj:`int` Hash of the block
            logsBloom: legacy
            miner: legacy
            mixHash: legacy
            nonce: legacy
            number: :obj:`int` Block number
            parentHash: legacy
            receiptsRoot: legacy
            sha3Uncles: legacy
            shardID :obj:`int` Shard ID
            stateRoot: legacy
            timestamp: legacy
            transactionsRoot: legacy
            viewID: View ID

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#7625493d-16bf-4611-8009-9635d063b4c0
    """
    method = "itcv2_getLatestChainHeaders"
    try:
        return rpc_request( method,
                            endpoint = endpoint,
                            timeout = timeout )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_by_number( # pylint: disable=too-many-arguments
    block_num,
    full_tx=False,
    include_tx=False,
    include_staking_tx=False,
    include_signers=False,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> dict:
    """Get block by number.

    Parameters
    ----------
    block_num: :obj:`int`
        Block number to fetch
    full_tx: :obj:`bool`, optional
        Include full transactions data for the block
    include_tx: :obj:`bool`, optional
        Include regular transactions for the block
    include_staking_tx: :obj:`bool`, optional
        Include staking transactions for the block
    include_signers: :obj:`bool`, optional
        Include list of signers for the block
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict with the following keys
        difficulty: legacy
        epoch: :obj:`int` Epoch number of block
        extraData: :obj:`str` Hex representation of extra data in the block
        gasLimit: :obj:`int` Maximum gas that can be used for transactions in the block
        gasUsed: :obj:`int` Gas that was actually used for transactions in the block
        hash: :obj:`str` Block hash
        logsBloom: :obj:`str` Bloom logs
        miner: :obj:`str` Wallet address of the leader that proposed this block
        mixHash: legacy
        nonce: legacy
        number: :obj:`int` Block number
        parentHash: :obj:`str` Hash of parent block
        receiptsRoot: :obj:`str` Hash of transaction receipt root
        signers: :obj:`list` List of signers (only if include_signers is set to True)
        size: :obj:`int` Block size in bytes
        stakingTransactions: :obj:`list`
            if full_tx is True: List of dictionaries,
                each containing a staking transaction (see account.get_staking_transaction_history)
            if full_tx is False: List of staking transaction hashes
        stateRoot: :obj:`str` Hash of state root
        timestamp: :obj:`int` Unix timestamp of the block
        transactions: :obj:`list`
            if full_tx is True: List of dictionaries,
                each containing a transaction (see account.get_transaction_history)
            if full_tx is False: List of transaction hashes
        transactionsRoot: :obj:`str` Hash of transactions root
        uncles: :obj:`str` legacy
        viewID: :obj:`int` View ID
        transactionsInEthHash: :obj:`str` Transactions in ethereum hash

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#52f8a4ce-d357-46f1-83fd-d100989a8243
    """
    params = [
        block_num,
        {
            "inclTx": include_tx,
            "fullTx": full_tx,
            "inclStaking": include_staking_tx,
            "withSigners": include_signers,
        },
    ]
    method = "itcv2_getBlockByNumber"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_by_hash( # pylint: disable=too-many-arguments
    block_hash,
    full_tx=False,
    include_tx=False,
    include_staking_tx=False,
    include_signers=False,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> dict:
    """Get block by hash.

    Parameters
    ----------
    block_hash: :obj:`str`
        Block hash to fetch
    full_tx: :obj:`bool`, optional
        Include full transactions data for the block
    include_tx: :obj:`bool`, optional
        Include regular transactions for the block
    include_staking_tx: :obj:`bool`, optional
        Include staking transactions for the block
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    See get_block_by_number for block structure

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#6a49ec47-1f74-4732-9f04-e5d76160bd5c
    """
    params = [
        block_hash,
        {
            "inclTx": include_tx,
            "fullTx": full_tx,
            "inclStaking": include_staking_tx,
            "withSigners": include_signers,
        },
    ]
    method = "itcv2_getBlockByHash"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_transaction_count_by_number(
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get transaction count for specific block number.

    Parameters
    ----------
    block_num: :obj:`int`
        Block number to get transaction count for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of transactions in the block

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#26c5adfb-d757-4595-9eb7-c6efef63df32
    """
    params = [ block_num ]
    method = "itcv2_getBlockTransactionCountByNumber"
    try:
        return int(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_transaction_count_by_hash(
    block_hash,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get transaction count for specific block hash.

    Parameters
    ----------
    block_hash: :obj:`str`
        Block hash to get transaction count
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of transactions in the block

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#66c68844-0208-49bb-a83b-08722bc113eb
    """
    params = [ block_hash ]
    method = "itcv2_getBlockTransactionCountByHash"
    try:
        return int(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_staking_transaction_count_by_number(
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get staking transaction count for specific block number.

    Parameters
    ----------
    block_num: :obj:`int`
        Block number to get transaction count for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of staking transactions in the block

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/transaction.go#L494
    """
    params = [ block_num ]
    method = "itcv2_getBlockStakingTransactionCountByNumber"
    try:
        return int(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_staking_transaction_count_by_hash(
    block_hash,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> int:
    """Get staking transaction count for specific block hash.

    Parameters
    ----------
    block_hash: :obj:`str`
        Block hash to get transaction count
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    include_full_tx: :obj:`bool`, optional
        Include list of full transactions data for each block
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int
        Number of transactions in the block

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/transaction.go#L523
    """
    params = [ block_hash ]
    method = "itcv2_getBlockStakingTransactionCountByHash"
    try:
        return int(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_blocks( # pylint: disable=too-many-arguments
    start_block,
    end_block,
    full_tx=False,
    include_tx=False,
    include_staking_tx=False,
    include_signers=False,
    endpoint=DEFAULT_ENDPOINT,
    timeout=DEFAULT_TIMEOUT,
) -> list:
    """Get list of blocks from a range.

    Parameters
    ----------
    start_block: :obj:`int`
        First block to fetch (inclusive)
    end_block: :obj:`int`
        Last block to fetch (inclusive)
    full_tx: :obj:`bool`, optional
        Include full transactions data for the block
    include_tx: :obj:`bool`, optional
        Include regular transactions for the block
    include_staking_tx: :obj:`bool`, optional
        Include staking transactions for the block
    include_signers: :obj:`bool`, optional
        Include list of signers for the block
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list of blocks, see get_block_by_number for block structure

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#ab9bdc59-e482-436c-ab2f-10df215cd0bd
    """
    params = [
        start_block,
        end_block,
        {
            "withSigners": include_signers,
            "fullTx": full_tx,
            "inclStaking": include_staking_tx,
            "inclTx": include_tx,
        },
    ]
    method = "itcv2_getBlocks"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_signers(
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> list:
    """Get list of block signers for specific block number.

    Parameters
    ----------
    block_num: :obj:`int`
        Block number to get signers for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        List of one addresses that signed the block

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#1e4b5f41-9db6-4dea-92fb-4408db78e622
    """
    params = [ block_num ]
    method = "itcv2_getBlockSigners"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_block_signers_keys(
    block_num,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> list:
    """Get list of block signer public bls keys for specific block number.

    Parameters
    ----------
    block_num: :obj:`int`
        Block number to get signer keys for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        List of bls public keys that signed the block

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#9f9c8298-1a4e-4901-beac-f34b59ed02f1
    """
    params = [ block_num ]
    method = "itcv2_getBlockSignerKeys"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def is_block_signer(
    block_num,
    address,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> bool:
    """Determine if the account at address is a signer for the block at
    block_num.

    Parameters
    ----------
    block_num: :obj:`int`
        Block number to check
    address: :obj:`str`
        Address to check
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    bool: True if the address was a signer for block_num, False otherwise

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/blockchain.go#L368
    """
    params = [ block_num, address ]
    method = "itcv2_isBlockSigner"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_signed_blocks(
    address,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> bool:
    """The number of blocks a particular validator signed for last blocksPeriod
    (1 epoch)

    Parameters
    ----------
    address: :obj:`str`
        Address to check
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    int: Number of blocks signed by account at address for last blocksPeriod

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://github.com/zennittians/intelchain/blob/1a8494c069dc3f708fdf690456713a2411465199/rpc/blockchain.go#L406
    """
    params = [ address ]
    method = "itcv2_getSignedBlocks"
    try:
        return int(
            rpc_request(
                method,
                params = params,
                endpoint = endpoint,
                timeout = timeout
            )[ "result" ]
        )
    except ( KeyError, TypeError ) as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_validators(
    epoch,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> dict:
    """Get list of validators for specific epoch number.

    Parameters
    ----------
    epoch: :obj:`int`
        Epoch to get list of validators for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    dict with the following keys
        shardID: :obj:`int` ID of the shard
        validators: :obj:`list` of dictionaries, each with the following keys
            address: :obj:`str` address of the validator
            balance: :obj:`int` balance of the validator in INTELLI

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#4dfe91ad-71fa-4c7d-83f3-d1c86a804da5
    """
    params = [ epoch ]
    method = "itcv2_getValidators"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception


def get_validator_keys(
    epoch,
    endpoint = DEFAULT_ENDPOINT,
    timeout = DEFAULT_TIMEOUT
) -> list:
    """Get list of validator public bls keys for specific epoch number.

    Parameters
    ----------
    epoch: :obj:`int`
        Epoch to get list of validator keys for
    endpoint: :obj:`str`, optional
        Endpoint to send request to
    timeout: :obj:`int`, optional
        Timeout in seconds

    Returns
    -------
    list
        List of bls public keys in the validator committee

    Raises
    ------
    InvalidRPCReplyError
        If received unknown result from endpoint

    API Reference
    -------------
    https://api.intelchain.org/#1439b580-fa3c-4d44-a79d-303390997a8c
    """
    params = [ epoch ]
    method = "itcv2_getValidatorKeys"
    try:
        return rpc_request(
            method,
            params = params,
            endpoint = endpoint,
            timeout = timeout
        )[ "result" ]
    except KeyError as exception:
        raise InvalidRPCReplyError( method, endpoint ) from exception
