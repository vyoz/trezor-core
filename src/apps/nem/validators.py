from apps.nem.helpers import *
from trezor.messages import NEMModificationType
from trezor.messages.NEMSignTx import NEMAggregateModification
from trezor.messages.NEMSignTx import NEMImportanceTransfer
from trezor.messages.NEMSignTx import NEMMosaicCreation
from trezor.messages.NEMSignTx import NEMMosaicSupplyChange
from trezor.messages.NEMSignTx import NEMProvisionNamespace
from trezor.messages.NEMSignTx import NEMSignTx
from trezor.messages.NEMSignTx import NEMTransactionCommon
from trezor.messages.NEMSignTx import NEMTransfer
from trezor.crypto import nem


def validate(msg: NEMSignTx):

    if msg.transaction is None:
        raise ValueError('No common provided')

    _validate_single_tx(msg)
    _validate_common(msg.transaction)

    if msg.transfer:
        _validate_transfer(msg.transfer, msg.transaction.network)
    if msg.provision_namespace:
        _validate_provision_namespace(msg.provision_namespace, msg.transaction.network)
    if msg.mosaic_creation:
        _validate_mosaic_creation(msg.mosaic_creation, msg.transaction.network)
    if msg.supply_change:
        _validate_supply_change(msg.supply_change)
    if msg.aggregate_modification:
        _validate_aggregate_modification(msg.aggregate_modification, msg.multisig is not None)
    if msg.importance_transfer:
        _validate_importance_transfer(msg.importance_transfer)


def validate_network(network: int) -> int:
    if network is None:
        return NEM_NETWORK_MAINNET
    _validate_network(network)
    return network


def _validate_network(network: int):
    if network not in [NEM_NETWORK_MAINNET, NEM_NETWORK_TESTNET, NEM_NETWORK_MIJIN]:
        raise ValueError('Invalid NEM network')


def _validate_single_tx(msg: NEMSignTx):
    # ensure exactly one transaction is provided
    tx_count = bool(msg.transfer) + \
               bool(msg.provision_namespace) + \
               bool(msg.mosaic_creation) + \
               bool(msg.supply_change) + \
               bool(msg.aggregate_modification) + \
               bool(msg.importance_transfer)
    if tx_count == 0:
        raise ValueError('No transaction provided')
    if tx_count > 1:
        raise ValueError('More than one transaction provided')


def _validate_common(common: NEMTransactionCommon, inner: bool=False):

    common.network = validate_network(common.network)

    err = None
    if common.timestamp is None:
        err = 'timestamp'
    if common.fee is None:
        err = 'fee'
    if common.deadline is None:
        err = 'deadline'

    is_signer = common.signer is not None
    if inner != is_signer:
        if not inner:
            raise ValueError('Signer not allowed in outer transaction')
        err = 'signer'

    if err:
        if inner:
            raise ValueError('No ' + err + ' provided in inner transaction')
        else:
            raise ValueError('No ' + err + ' provided')

    if common.signer is not None:
        _validate_public_key(common.signer, 'Invalid signer public key in inner transaction')


def _validate_public_key(public_key: bytes, err_msg):
    if not public_key:
        raise ValueError(err_msg + ' (none provided)')
    if len(public_key) != NEM_PUBLIC_KEY_SIZE:
        raise ValueError(err_msg + ' (invalid length)')


def _validate_importance_transfer(importance_transfer: NEMImportanceTransfer):
    if importance_transfer.mode is None:
        raise ValueError('No mode provided')
    _validate_public_key(importance_transfer.public_key, 'Invalid remote account public key provided')


def _validate_aggregate_modification(aggregate_modification: NEMAggregateModification, creation: bool=False):

    if creation and len(aggregate_modification.modifications) == 0:
        raise ValueError('No modifications provided')

    for m in aggregate_modification.modifications:
        if not m.type:
            raise ValueError('No modification type provided')
        if m.type not in [
            NEMModificationType.CosignatoryModification_Add,
            NEMModificationType.CosignatoryModification_Delete
        ]:
            raise ValueError('Unknown aggregate modification ')
        if creation and m.type == NEMModificationType.CosignatoryModification_Delete:
            raise ValueError('Cannot remove cosignatory when converting account')
        _validate_public_key(m.public_key, 'Invalid cosignatory public key provided')


def _validate_supply_change(supply_change: NEMMosaicSupplyChange):
    if supply_change.namespace is None:
        raise ValueError('No namespace provided')
    if supply_change.mosaic is None:
        raise ValueError('No mosaic provided')
    if supply_change.type is None:
        raise ValueError('No type provided')
    if supply_change.delta is None:
        raise ValueError('No delta provided')


def _validate_mosaic_creation(mosaic_creation: NEMMosaicCreation, network: int):
    if mosaic_creation.definition is None:
        raise ValueError('No mosaic definition provided')
    if mosaic_creation.sink is None:
        raise ValueError('No creation sink provided')
    if mosaic_creation.fee is None:
        raise ValueError('No creation sink fee provided')

    if not nem.validate_address(mosaic_creation.sink, network):
        raise ValueError('Invalid creation sink address')

    if mosaic_creation.definition.name is not None:
        raise ValueError('Name not allowed in mosaic creation transactions')
    if mosaic_creation.definition.ticker is not None:
        raise ValueError('Ticker not allowed in mosaic creation transactions')
    if len(mosaic_creation.definition.networks):
        raise ValueError('Networks not allowed in mosaic creation transactions')

    if mosaic_creation.definition.namespace is None:
        raise ValueError('No mosaic namespace provided')
    if mosaic_creation.definition.mosaic is None:
        raise ValueError('No mosaic name provided')

    if mosaic_creation.definition.supply is not None and mosaic_creation.definition.divisibility is None:
            raise ValueError('Definition divisibility needs to be provided when supply is')
    if mosaic_creation.definition.supply is None and mosaic_creation.definition.divisibility is not None:
            raise ValueError('Definition supply needs to be provided when divisibility is')

    if mosaic_creation.definition.levy is not None:
        if mosaic_creation.definition.fee is None:
            raise ValueError('No levy fee provided')
        if mosaic_creation.definition.levy_address is None:
            raise ValueError('No levy address provided')
        if mosaic_creation.definition.levy_namespace is None:
            raise ValueError('No levy namespace provided')
        if mosaic_creation.definition.levy_mosaic is None:
            raise ValueError('No levy mosaic name provided')

        if mosaic_creation.definition.divisibility is None:
            raise ValueError('No divisibility provided')
        if mosaic_creation.definition.supply is None:
            raise ValueError('No supply provided')
        if mosaic_creation.definition.mutable_supply is None:
            raise ValueError('No supply mutability provided')
        if mosaic_creation.definition.transferable is None:
            raise ValueError('No mosaic transferability provided')
        if mosaic_creation.definition.description is None:
            raise ValueError('No description provided')

        if mosaic_creation.definition.divisibility > NEM_MAX_DIVISIBILITY:
            raise ValueError('Invalid divisibility provided')
        if mosaic_creation.definition.supply > NEM_MAX_SUPPLY:
            raise ValueError('Invalid supply provided')

        if not nem.validate_address(mosaic_creation.definition.levy_address, network):
            raise ValueError('Invalid levy address')


def _validate_provision_namespace(provision_namespace: NEMProvisionNamespace, network: int):
    if provision_namespace.namespace is None:
        raise ValueError('No namespace provided')
    if provision_namespace.sink is None:
        raise ValueError('No rental sink provided')
    if provision_namespace.fee is None:
        raise ValueError('No rental sink fee provided')

    if not nem.validate_address(provision_namespace.sink, network):
        raise ValueError('Invalid rental sink address')


def _validate_transfer(transfer: NEMTransfer, network: int):
    if transfer.recipient is None:
        raise ValueError('No recipient provided')
    if transfer.amount is None:
        raise ValueError('No amount provided')

    if transfer.public_key is not None:
        _validate_public_key(transfer.public_key, 'Invalid recipient public key')

    if not nem.validate_address(transfer.recipient, network):
        raise ValueError('Invalid recipient address')

    for m in transfer.mosaics:
        if m.namespace is None:
            raise ValueError('No mosaic namespace provided')
        if m.mosaic is None:
            raise ValueError('No mosaic name provided')
        if m.quantity is None:
            raise ValueError('No mosaic quantity provided')
