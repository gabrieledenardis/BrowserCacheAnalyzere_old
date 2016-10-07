# -*- coding: utf-8 -*-
# !/usr/bin/env python


# Python imports
import struct
import binascii
import urllib

# Project imports
from utilities import utils
import cache_file
import cache_resource


class CacheEntry(object):

    def __init__(self, cache_path=None, entry_file=None, block_dimension=None, block_number=None):
        """

        :param cache_path: path containing "chrome" cache
        :param entry_file: file containing the entry
        :param block_dimension: dimension of the block within the file (depending on data_# file)
        :param block_number: number of the block within the file
        """

        self.cache_path = cache_path
        self.entry_file = entry_file
        self.block_dimension = block_dimension
        self.block_number = block_number

        data_header_dimension = 8192

        self.key_data = ""

        with open(self.entry_file, "rb") as f_entry:

            f_entry.seek(data_header_dimension + (self.block_dimension * self.block_number))

            # Entry fields
            self.key_hash = struct.unpack("<I", f_entry.read(4))[0]
            self.next_entry_address = struct.unpack("<I", f_entry.read(4))[0]
            self.rankings_node_address = format(struct.unpack("<I", f_entry.read(4))[0], "032b")
            self.reuse_count = struct.unpack("<I", f_entry.read(4))[0]
            self.refetch_count = struct.unpack("<I", f_entry.read(4))[0]
            self.entry_state = entry_state_selector[struct.unpack("<I", f_entry.read(4))[0]]
            self.creation_time = utils.webkit_to_unix_timestamp(hex(struct.unpack("<Q", f_entry.read(8))[0]))
            self.key_data_size = struct.unpack("<I", f_entry.read(4))[0]
            self.long_key_data_address = struct.unpack("<I", f_entry.read(4))[0]

            # Array of data stream size
            self.data_stream_sizes = []
            for s_size in range(4):
                self.stream_size = struct.unpack("<I", f_entry.read(4))[0]
                self.data_stream_sizes.append(self.stream_size)

            # Array of data stream cache addresses
            self.data_stream_addresses = []

            for s_address in range(4):
                self.stream_address = format(struct.unpack("<I", f_entry.read(4))[0], "032b")

                # Valid and existing address (valid = most significant bit == 1)
                if self.stream_address and self.stream_address[0] == "1":
                    self.stream_address_instance = cache_file.CacheFile(binary_address=self.stream_address,
                                                                        cache_path=self.cache_path)

                    # Array index for HTTP Response Header
                    if s_address == 0:
                        self.cache_resource_instance = \
                            cache_resource.CacheResource(resource_file=self.stream_address_instance.file_path,
                                                         file_type=self.stream_address_instance.file_type,
                                                         block_dimension=self.stream_address_instance.block_dimension,
                                                         block_number=self.stream_address_instance.block_number,
                                                         resource_size=self.data_stream_sizes[s_address],
                                                         is_http_header=True)
                    # Not HTTP Response Header
                    else:
                        self.cache_resource_instance = \
                            cache_resource.CacheResource(resource_file=self.stream_address_instance.file_path,
                                                         file_type=self.stream_address_instance.file_type,
                                                         block_dimension=self.stream_address_instance.block_dimension,
                                                         block_number=self.stream_address_instance.block_number,
                                                         resource_size=self.data_stream_sizes[s_address],
                                                         is_http_header=False)
                    self.entry_data = self.cache_resource_instance.resource_data
                    self.data_stream_addresses.insert(s_address, self.cache_resource_instance)
                # Not valid and existing address
                else:
                    self.data_stream_addresses.insert(s_address, None)
            # Cache entry flags
            self.cache_entry_flags = struct.unpack("<I", f_entry.read(4))[0]

            # Skipping padding
            f_entry.seek(16, 1)

            # The hash of the entry up to this point
            self.self_hash = struct.unpack("<I", f_entry.read(4))[0]

            # Reading key
            # If zero, key is local
            if self.long_key_data_address == 0:

                for c in range(self.key_data_size):
                    self.key_data += binascii.b2a_qp(f_entry.read(1))

                # Unquote and replacement for not standard percent-encoding escape sequences found in http header
                self.key_data = urllib.unquote(self.key_data.replace("=2E", ".").replace("=20", " ")
                                               .replace("=3D", "="))

                # Replacing eventual end-of string character (=00)
                self.key_data = self.key_data.replace("=00", "")

            # address of key_data
            else:
                self.key_file_instance = cache_file.CacheFile(binary_address=format(self.long_key_data_address, "032b"),
                                                              cache_path=self.cache_path)

                self.key_resource_instance = \
                    cache_resource.CacheResource(resource_file=self.key_file_instance.file_path,
                                                 file_type=self.key_file_instance.file_type,
                                                 block_dimension=self.key_file_instance.block_dimension,
                                                 block_number=self.key_file_instance.block_number,
                                                 resource_size=self.key_data_size,
                                                 is_http_header="Unknown")
                self.key_data = self.key_resource_instance.resource_data


# State of cache entry
entry_state_selector = {
    0: "Entry Normal",
    1: "Entry Evicted",
    2: "Entry Doomed"
}
