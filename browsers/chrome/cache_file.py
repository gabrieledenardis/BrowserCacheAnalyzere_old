# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os


class CacheFile(object):

    def __init__(self, binary_address=None, cache_path=None):
        """

        :param binary_address: 32 bits address from "index file" address table
        :param cache_path: path containing "chrome" cache
        """

        self.bin_address = binary_address
        self.cache_folder = cache_path

        # Cache file type (Bits 1-3 in binary address)
        self.file_type = self.bin_address[1:4]

        # Number of contiguous blocks in data_ file (Bits 6-7 in binary address)
        self.block_size = None

        # File selector (Number of # in data_#) (Bits 8-15 in binary address)
        self.file_number = None

        # Block number (Bits 16-32 in binary address)
        self.block_number = None

        # Block dimension corresponding for each data_ file
        self.block_dimension = block_dimension_selector[self.file_type]

        # Cache file name (data_# or f_######)
        self.file_name = None

        # Complete path to cache file
        self.file_path = None

        # Separate file
        if self.file_type == "000":
            self.file_number = int(self.bin_address[4:], 2)
            self.file_name = "f_" + str(format(self.file_number, "06x"))
            self.file_path = os.sep.join([self.cache_folder, self.file_name])
        # Data_ file
        else:
            self.block_size = int(self.bin_address[6:8], 2)
            self.file_number = int(self.bin_address[8:16], 2)
            self.block_number = int(self.bin_address[16:], 2)
            self.file_name = "data_" + str(self.file_number)
            self.file_path = os.sep.join([self.cache_folder, self.file_name])

# Block dimension (in byte) for each data_# file
block_dimension_selector = {
        "000": 0,  # Separate file
        "001": 36,  # Rankings node data_0
        "010": 256,  # data_1
        "011": 1024,  # data_2
        "100": 4096  # data_3
    }
