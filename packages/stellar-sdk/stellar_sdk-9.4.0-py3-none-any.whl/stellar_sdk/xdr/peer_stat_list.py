# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .peer_stats import PeerStats

__all__ = ["PeerStatList"]


class PeerStatList:
    """
    XDR Source Code::

        typedef PeerStats PeerStatList<25>;
    """

    def __init__(self, peer_stat_list: List[PeerStats]) -> None:
        _expect_max_length = 25
        if peer_stat_list and len(peer_stat_list) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `peer_stat_list` should be {_expect_max_length}, but got {len(peer_stat_list)}."
            )
        self.peer_stat_list = peer_stat_list

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.peer_stat_list))
        for peer_stat_list_item in self.peer_stat_list:
            peer_stat_list_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> PeerStatList:
        length = unpacker.unpack_uint()
        peer_stat_list = []
        for _ in range(length):
            peer_stat_list.append(PeerStats.unpack(unpacker))
        return cls(peer_stat_list)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PeerStatList:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PeerStatList:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.peer_stat_list)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.peer_stat_list == other.peer_stat_list

    def __str__(self):
        return f"<PeerStatList [peer_stat_list={self.peer_stat_list}]>"
