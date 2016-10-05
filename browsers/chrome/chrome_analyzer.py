# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Python imports
import os
import struct
from threading import Event

# Project imports
import index_header
import cache_file
import cache_entry


class ChromeAnalyzerThread(QtCore.QThread):
    """
    Analyzer for Google Chrome cache and Opera cache.
    """

    def __init__(self, parent=None, input_path=None):
        super(ChromeAnalyzerThread, self).__init__(parent)

        self.stop_signal = Event()
        self.input_path = input_path

    def __del__(self):
        self.wait()

    def run(self):

        # Chrome "index" file
        index_file = os.path.join(self.input_path, "index")

        # Dimension of header in cache "index" file
        index_header_dimension = 368

        # Address table size in "index" file
        table_size = index_header.read_index_file(index_file)["table_size"]

        # List of all cache entries found
        cache_entries_list = []

        with open(index_file, "rb") as f_index:

            # Skipping index header
            f_index.seek(index_header_dimension)

            for addresses in range(table_size):
                if self.stop_signal.is_set():
                    print "STOP!"
                    break
                # Binary address (32 bits)
                bin_address_in_index = format(struct.unpack("<I", f_index.read(4))[0], "032b")

                # Existing and valid entry (valid = most significant bit == 1)
                if bin_address_in_index and bin_address_in_index[0] == "1":

                    # Entry location
                    cache_file_instance = cache_file.CacheFile(binary_address=bin_address_in_index,
                                                               cache_path=self.input_path)

                    cache_entry_instance = cache_entry.CacheEntry(cache_path=self.input_path,
                                                                  entry_file=cache_file_instance.file_path,
                                                                  block_dimension=cache_file_instance.block_dimension,
                                                                  block_number=cache_file_instance.block_number)

                    # If an entry has a valid next entry address (an entry with the same hash),
                    # adding it to the entries list. Those entries are not in index table addresses
                    while cache_entry_instance.next_entry_address != 0:
                        # Adds cache entry to cache entries list
                        cache_entries_list.append(cache_entry_instance)

                        # Next entry address (from current entry)
                        bin_next_entry_address = format(cache_entry_instance.next_entry_address, "032b")

                        # Corresponding entry location (from next entry address)
                        cache_next_file_instance = cache_file.CacheFile(binary_address=bin_next_entry_address,
                                                                        cache_path=self.input_path)
                        cache_entry_instance = \
                            cache_entry.CacheEntry(cache_path=self.input_path,
                                                   entry_file=cache_next_file_instance.file_path,
                                                   block_dimension=cache_next_file_instance.block_dimension,
                                                   block_number=cache_next_file_instance.block_number)

                    # Adds cache entry to cache entries list
                    cache_entries_list.append(cache_entry_instance)
