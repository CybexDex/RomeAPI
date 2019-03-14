from collections import OrderedDict
from graphenebase.types import (Bool, PointInTime, Set, Int64, Map, Id, VoteId)
from graphenebase.objects import GrapheneObject, isArgsThisClass#, Asset
from graphenebase.objects import ObjectId as GPHObjectId

from .objecttypes import object_type
from .objects import LimitOrderCancelExtensions

# class ObjectId(GPHObjectId):
#     """ Need to overwrite a few attributes to load proper object_types from
#         bitshares
#     """
#
#     object_types = object_type


def AssetId(asset):
    return ObjectId(asset, "asset")


def AccountId(asset):
    return ObjectId(asset, "account")


class ObjectId(GPHObjectId):
    """ Encodes object/protocol ids
    """
    def __init__(self, object_str, type_verify=None):
        if len(object_str.split(".")) == 3:
            space, type, id = object_str.split(".")
            self.space = int(space)
            self.type = int(type)
            self.instance = Id(int(id))
            self.Id = object_str
            if type_verify:
                assert object_type[type_verify] == int(type),\
                    "Object id does not match object type! " +\
                    "Excpected %d, got %d" %\
                    (object_type[type_verify], int(type))
        else:
            raise Exception("Object id is invalid")

# # Common Objects
# class Asset(GrapheneObject):
#     def __init__(self, *args, **kwargs):
#         if isArgsThisClass(self, args):
#             self.data = args[0].data
#         else:
#             if len(args) == 1 and len(kwargs) == 0:
#                 kwargs = args[0]
#             super().__init__(
#                 OrderedDict(
#                     [
#                         ("amount", Int64(kwargs["amount"])),
#                         ("asset_id", ObjectId(kwargs["asset_id"], "asset")),
#                     ]
#                 )
#             )


class Asset(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('amount', Int64(kwargs["amount"])),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset"))
            ]))


class Limit_order_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                            ("fee", Asset(kwargs["fee"])),
                            ("seller", ObjectId(kwargs["seller"], "account")),
                            ("amount_to_sell", Asset(kwargs["amount_to_sell"])),
                            ("min_to_receive", Asset(kwargs["min_to_receive"])),
                            ("expiration", PointInTime(kwargs["expiration"])),
                            ("fill_or_kill", Bool(kwargs["fill_or_kill"])),
                            ("extensions", Set([])),
                    ]
                )
            )

# bitshares implementations
# class Limit_order_cancel(GrapheneObject):
#     def __init__(self, *args, **kwargs):
#         if isArgsThisClass(self, args):
#             self.data = args[0].data
#         else:
#             if len(args) == 1 and len(kwargs) == 0:
#                 kwargs = args[0]
#             super().__init__(
#                 OrderedDict(
#                     [
#                         ("fee", Asset(kwargs["fee"])),
#                         (
#                             "fee_paying_account",
#                             ObjectId(kwargs["fee_paying_account"], "account"),
#                         ),
#                         ("order", ObjectId(kwargs["order"], "limit_order")),
#                         ("extensions", Set([])),
#                     ]
#                 )
#             )

class Limit_order_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            if 'extensions' not in kwargs or not kwargs['extensions']:
                kwargs['extensions'] = []
            elif not isinstance(kwargs['extensions'], list):
                raise TypeError('You need to provide a list as extension param')

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('order', ObjectId(kwargs["order"], "limit_order")),
                ('extensions', LimitOrderCancelExtensions(kwargs['extensions'])),
            ]))

class Cancel_all(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('seller', ObjectId(kwargs["seller"], "account")),
                ('sell_asset_id', ObjectId(kwargs["sell_asset_id"], "asset")),
                ('receive_asset_id', ObjectId(kwargs["receive_asset_id"], "asset")),
                ('extensions', Set([]))
            ]))
