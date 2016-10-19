# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore

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

    update_results_table_signal = QtCore.pyqtSignal(int, int, str, str, str, str)

    def __init__(self, parent=None, input_path=None):
        super(ChromeAnalyzerThread, self).__init__(parent)

        self.input_path = input_path

        # Signal from "stop analysis" button
        self.stop_signal_analyzer = Event()

        # List of all cache entries found
        self.cache_entries_list = []

        # Checking if thread stopped by user
        self.stopped_by_user = False

    def run(self):

        # Chrome "index" file
        index_file = os.path.join(self.input_path, "index")

        # Dimension of header in cache "index" file
        index_header_dimension = 368

        # Address table size in "index" file
        table_size = index_header.read_index_header(index_file)["table_size"]

        num_entries = index_header.read_index_header(index_file)["number_of_entries"]

        with open(index_file, "rb") as f_index:

            # Skipping index header
            f_index.seek(index_header_dimension)

            for addresses in range(table_size):
                # If "stop analysis" button is clicked, stopping analysis
                if self.stop_signal_analyzer.is_set():
                    self.stopped_by_user = True
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

                        if (cache_entry_instance.data_stream_addresses[0] and
                                isinstance(cache_entry_instance.data_stream_addresses[0].resource_data, dict)):

                            if "Content-Type" in cache_entry_instance.data_stream_addresses[0].resource_data:
                                self.update_results_table_signal.emit(len(self.cache_entries_list) - 1,
                                                                      num_entries,
                                                                      str(cache_entry_instance.key_hash),
                                                                      cache_entry_instance.key_data,
                                                                      cache_entry_instance.data_stream_addresses[
                                                                          0].resource_data['Content-Type'],
                                                                      cache_entry_instance.creation_time)
                            else:
                                self.update_results_table_signal.emit(len(self.cache_entries_list) - 1,
                                                                      num_entries,
                                                                      str(cache_entry_instance.key_hash),
                                                                      cache_entry_instance.key_data,
                                                                      "Not present",
                                                                      cache_entry_instance.creation_time)
                        else:
                            self.update_results_table_signal.emit(len(self.cache_entries_list) - 1,
                                                                  num_entries,
                                                                  str(cache_entry_instance.key_hash),
                                                                  cache_entry_instance.key_data,
                                                                  "Unknown",
                                                                  cache_entry_instance.creation_time)
                        # Adds cache entry to cache entries list
                        self.cache_entries_list.append(cache_entry_instance)

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

                    # Adding cache entry to cache entries list
                    self.cache_entries_list.append(cache_entry_instance)

                    if (cache_entry_instance.data_stream_addresses[0] and
                            isinstance(cache_entry_instance.data_stream_addresses[0].resource_data, dict)):

                            if "Content-Type" in cache_entry_instance.data_stream_addresses[0].resource_data:
                                self.update_results_table_signal.emit(len(self.cache_entries_list)-1,
                                                                      num_entries,
                                                                      str(cache_entry_instance.key_hash),
                                                                      cache_entry_instance.key_data,
                                                                      cache_entry_instance.data_stream_addresses[0].resource_data['Content-Type'],
                                                                      cache_entry_instance.creation_time)
                            else:
                                self.update_results_table_signal.emit(len(self.cache_entries_list)-1,
                                                                      num_entries,
                                                                      str(cache_entry_instance.key_hash),
                                                                      cache_entry_instance.key_data,
                                                                      "Not present",
                                                                      cache_entry_instance.creation_time)
                    else:
                        self.update_results_table_signal.emit(len(self.cache_entries_list) - 1,
                                                              num_entries,
                                                              str(cache_entry_instance.key_hash),
                                                              cache_entry_instance.key_data,
                                                              "Unknown",
                                                              cache_entry_instance.creation_time)

        print "finito analyzer"