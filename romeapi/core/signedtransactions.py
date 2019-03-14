import json
# -*- coding: utf-8 -*-
from graphenebase.signedtransactions import (
    Signed_Transaction as GrapheneSigned_Transaction,
)
from graphenebase.objects import Operation as GPHOperation
from .operationids import operations
# from .chains import known_chains


class Operation(GPHOperation):
    def __init__(self, *args, **kwargs):
        super(Operation, self).__init__(*args, **kwargs)

    def _getklass(self, name):
        module = __import__("bitsharesbase.operations", fromlist=["operations"])
        class_ = getattr(module, name)
        return class_

    def operations(self):
        return operations

    def getOperationNameForId(self, i):
        """ Convert an operation id into the corresponding string
        """
        for key in operations:
            if int(operations[key]) is int(i):
                return key
        return "Unknown Operation ID %d" % i

    def json(self):
        return json.loads(str(self))

# class Signed_Transaction(GrapheneSigned_Transaction):
#     """ Create a signed transaction and offer method to create the
#         signature
#         :param num refNum: parameter ref_block_num (see ``getBlockParams``)
#         :param num refPrefix: parameter ref_block_prefix (see ``getBlockParams``)
#         :param str expiration: expiration date
#         :param Array operations:  array of operations
#     """
#
#     known_chains = {
#         "PROD": {
#             "chain_id": "90be01e82b981c8f201c9a78a3d31f655743b29ff3274727b1439b093d04aa23",
#             "core_symbol": "CYB",
#             "prefix": "CYB",
#         }
#     }
#     default_prefix = "CYB"
#     operation_klass = Operation

class Signed_Transaction(GrapheneSigned_Transaction):
    """ Create a signed transaction and offer method to create the
        signature

        :param num refNum: parameter ref_block_num (see ``getBlockParams``)
        :param num refPrefix: parameter ref_block_prefix (see ``getBlockParams``)
        :param str expiration: expiration date
        :param Array operations:  array of operations
    """
    def __init__(self, *args, **kwargs):
        super(Signed_Transaction, self).__init__(*args, **kwargs)


    def getOperationKlass(self):
        return Operation

    def getKnownChains(self):
        known_chains = {
            "PROD": {
                "chain_id": "90be01e82b981c8f201c9a78a3d31f655743b29ff3274727b1439b093d04aa23",
                "core_symbol": "CYB",
                "prefix": "CYB",
            }
        }

        return known_chains
