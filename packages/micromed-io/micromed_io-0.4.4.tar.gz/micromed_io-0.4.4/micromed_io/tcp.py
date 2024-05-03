"""Micromed TCP module."""

import sys
from enum import IntEnum
import struct
import numpy as np

import logging

from micromed_io.in_out import MicromedIO


class MicromedPacketType(IntEnum):
    """Micromed packet type."""

    HEADER = 0
    EEG_DATA = 1
    NOTE = 2
    MARKER = 3


def get_tcp_header(packet_type: MicromedPacketType, size: int) -> bytearray:
    """Build the Micromed TCP header

    Parameters
    ----------
    packet_type : MicromedPacketType
        The packet type to be sent
    size : int
        The size of the packet to be sent

    Returns
    -------
    bytearray
        The TCP header sent right before any packet
    """
    tcp_header = bytearray(b"MICM")
    tcp_header.extend((packet_type).to_bytes(2, byteorder="little"))
    tcp_header.extend(size.to_bytes(4, byteorder="little"))
    return tcp_header


def decode_tcp_header_packet(packet: bytearray):
    """Decode the Micromed tcp header packet.

    Parameters
    ----------
    packet : bytearray
        The tcp packet to decode.

    Returns
    -------
    bool
        True if decoding was successful. Else False.
    """
    packet_type = None
    next_packet_size = None
    if len(packet) > 0:
        # Check that the packet is not corrupted
        if packet[:4].decode() == "MICM":
            packet_type = int.from_bytes(packet[4:6], "little")
            next_packet_size = int.from_bytes(packet[6:10], "little")
        else:
            logging.warning(f"Wrong header packet: {packet.decode()}")
    else:
        logging.warning(f"header empty packet: [{packet.decode()}]")
    return packet_type, next_packet_size


def decode_tcp_marker_packet(packet: bytearray):
    """Decode the Micromed tcp markers packet.

    Parameters
    ----------
    packet : bytearray
        The tcp packet to decode.

    Returns
    -------
    tuple
        trigger_sample: the sample when the marker is received
        trigger_value: trigger value
    """

    trigger_sample = int.from_bytes(packet[:4], byteorder="little")
    trigger_value = int.from_bytes(packet[4:6], byteorder="little")
    return trigger_sample, trigger_value


def decode_tcp_note_packet(packet: bytearray):
    """Decode the Micromed tcp markers packet.

    Parameters
    ----------
    packet : bytearray
        The tcp packet to decode.

    Returns
    -------
    tuple
        trigger_sample: the sample when the marker is received
        trigger_value: trigger value
    """

    note_sample = struct.unpack("<I", packet[:4])
    note_value = packet[4:].decode(encoding="utf-8").rstrip("\x00")
    return note_sample, note_value


def encode_note_packet(sample: np.uint32, note: str) -> bytearray:
    """Encode a note packet with sample and text

    Parameters
    ----------
    sample : np.uint32
        The sample when note occured
    note : str
        The text

    Returns
    -------
    bytearray
        The encoded packet
    """
    packet = struct.pack("<I", sample)
    packet += struct.pack("<40s", (note).encode(encoding="utf-8"))
    return packet


def encode_marker_packet(sample: np.uint32, marker: np.uint16) -> bytearray:
    """Encode a marker packet with sample and value

    Parameters
    ----------
    sample : np.uint32
        The sample when marker occured
    marker : np.uint16
        The marker value

    Returns
    -------
    bytearray
        The encoded packet
    """
    packet = struct.pack("<I", sample)
    packet += struct.pack("<H", marker)
    return packet
