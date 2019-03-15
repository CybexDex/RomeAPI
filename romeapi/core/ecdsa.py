from binascii import hexlify
from graphenebase.base58 import Base58
import sys
import hashlib

from coincurve._libsecp256k1 import ffi as CCffi, lib as CClib
from coincurve.context import GLOBAL_CONTEXT as CCGLOBAL_CONTEXT
import coincurve.utils as CCutils
from graphenebase.ecdsa import _is_canonical

# skip public key calculation, speeding up
class QuickPrivateKey(object):
    def __init__(self, wif = None, prefix = "GPH"):
        if wif is None:
            import os
            self._wif = Base58(hexlify(os.urandom(32)).decode('ascii'))
        elif isinstance(wif, QuickPrivateKey):
            self._wif = wif._wif
        elif isinstance(wif, Base58):
            self._wif = wif
        else:
            self._wif = Base58(wif)

    def __repr__(self):
        return repr(self._wif)

    def __bytes__(self):
        if sys.version > '3':
            return bytes(self._wif)
        else:
            return self._wif.__bytes__()
#
# def sign_message(message, wif, hashfn=hashlib.sha256):
#     if not isinstance(message, bytes):
#         message = bytes(message, "utf-8")
#
#     msg_hash = hashfn(message).digest()
#
#     priv_key = QuickPrivateKey(wif)
#     secret = bytes(priv_key)
#     # if ctx is None:
#     #     assert flags in (NO_FLAGS, FLAG_SIGN, FLAG_VERIFY, ALL_FLAGS)
#     #     ctx = lib.secp256k1_context_create(flags)
#
#     context = GLOBAL_CONTEXT
#
#     if len(msg_hash) != 32:
#         raise ValueError('Message hash must be 32 bytes long.')
#
#     ndata = ffi.new("const int *ndata")
#     ndata[0] = 0
#
#     while True:
#         sig = ffi.new('secp256k1_ecdsa_recoverable_signature *')
#
#         signed = lib.secp256k1_ecdsa_sign_recoverable(
#             # privkey.ctx, sig, digest, privkey.private_key, secp256k1.ffi.NULL, ndata
#             context.ctx, sig, msg_hash, secret, ffi.NULL, ndata
#         )
#
#         if not signed:
#             raise ValueError('The nonce generation function failed, or the private key was invalid.')
#
#         signature, i = ecdsa_recoverable_serialize(sig, context)
#
#         if _is_canonical(signature):
#             i += 4  # compressed
#             i += 27  # compact
#             break
#
#     sigstr = struct.pack("<B", i)
#     sigstr += signature
#
#     return sigstr


def quick_sign_message(message, wif, hashfn=hashlib.sha256):
    if not isinstance(message, bytes):
        message = bytes(message, "utf-8")

    digest = hashfn(message).digest()
    priv_key = QuickPrivateKey(wif)
    if sys.version > '3':
        p = bytes(priv_key)
    else:
        p = bytes(priv_key.__bytes__())

    ndata = CCffi.new("const int *ndata")
    ndata[0] = 0
    while True:
        ndata[0] += 1
        signature = CCffi.new('secp256k1_ecdsa_recoverable_signature *')
        signed = CClib.secp256k1_ecdsa_sign_recoverable(
            CCGLOBAL_CONTEXT.ctx,
            signature,
            digest, p, CCffi.NULL, ndata
        )

        if not signed:
            raise AssertionError()

        output = CCffi.new('unsigned char[%d]' % 64)
        recid = CCffi.new('int *')

        CClib.secp256k1_ecdsa_recoverable_signature_serialize_compact(
            CCGLOBAL_CONTEXT.ctx,
            output,
            recid,
            signature)

        output_sig = CCffi.buffer(output, 64)

        if _is_canonical(output_sig):
            return bytes(
                CCutils.int_to_bytes(31 + recid[0]) +
                output_sig)
