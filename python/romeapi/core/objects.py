from graphenebase.types import (Set, Bool, Static_variant)
from .cybex_types import Ripemd160

from collections import OrderedDict
from graphenebase.objects import GrapheneObject, isArgsThisClass

class LimitOrderCreateExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions ############################
        class Order_side_ext(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('is_buy', Bool(kwargs['is_buy']))
                    ]))
        # End of Extensions definition ##########
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
        if len(kwargs) == 0:
            return super().__init__([])
        a = []
        ext = kwargs[0]
        assert ext[0] == 7
        a.append(Static_variant(
            Order_side_ext(ext[1]),
            ext[0]
        ))
        super().__init__(a)

class LimitOrderCancelExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions ############################
        class Cancel_trx_id_ext(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('trx_id', Ripemd160(kwargs['trx_id']))
                    ]))
        # End of Extensions definition ##########
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        if len(kwargs) == 0:
            return super().__init__([])

        a = []
        ext = kwargs[0]
        assert ext[0] == 6
        a.append(Static_variant(
            Cancel_trx_id_ext(ext[1]),
            ext[0]
        ))
        super().__init__(a)
