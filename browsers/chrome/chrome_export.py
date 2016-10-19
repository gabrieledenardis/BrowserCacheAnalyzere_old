# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore

# Python imports
import os
import datetime
import platform
import shutil
from threading import Event
import webbrowser

# Project imports
from utilities import utils
import index_header
import data_header


class ChromeExportThread(QtCore.QThread):
    update_export_progress_signal = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None, input_path=None, output_path=None, scan_main_folder_name=None,
                 entries_to_export=None,
                 brw=None, brw_ver=None, brw_inst_path=None, brw_def_path=None):

        super(ChromeExportThread, self).__init__(parent)

        # Signal from "stop analysis" button
        self.stop_signal_export = Event()

        # Checking if thread stopped by user
        self.stopped_by_user = False

        # External values
        self.input_path = input_path
        self.output_path = output_path
        self.scan_main_folder_name = scan_main_folder_name
        self.browser = brw,
        self.browser_version = brw_ver,
        self.browser_inst_path = brw_inst_path,
        self.browser_def_path = brw_def_path,
        self.entries_to_export = entries_to_export

        self.stopped_by_user = False

    def run(self):
        # TODO:utc time?
        # TODO:readonly dirs?

        # Current time
        current_datetime = datetime.datetime.now().strftime("%d-%b-%Y-%H_%M_%S")
        current_datetime_extended = datetime.datetime.now().strftime("%A - %d %B %Y - %H:%M:%S")

        # Report folders
        scan_report_folder_name = "Scan_report"
        scan_results_folder_name = "Scan_results"

        # Paths for results folder
        scan_report_path = os.path.join(self.output_path, self.scan_main_folder_name, scan_report_folder_name)
        scan_results_path = os.path.join(self.output_path, self.scan_main_folder_name, scan_results_folder_name)

        # HTML index in scan report folder
        scan_report_index = os.path.join(scan_report_path, "index.html")
        scan_results_index = os.path.join(scan_results_path, "index.html")

        # System info
        os_name = platform.system()
        os_rel = platform.release()
        os_rel_ver = platform.version()
        hostname = platform.node()

        # Cache folder info
        folder_info = utils.get_folder_info(folder_path=self.input_path)

        # Chrome index file info
        chrome_index_file = os.path.join(self.input_path, "index")
        chrome_index_header = index_header.read_index_header(index_to_open=chrome_index_file)
        chrome_index_info = utils.get_file_info(file_path=chrome_index_file)

        # Creating scan results folder
        try:
            os.makedirs(scan_report_path)
            os.makedirs(scan_results_path)
        except Exception as _:
            pass
            # TODO:exceptions

        ########################
        # SECTION: SCAN REPORT #
        ########################

        html_string_report_open_page = """
        <html>
        <head> <title> {scan_date} </title> </head>
        <body>
        """.format(
            scan_date=current_datetime
        )

        html_string_report_info = """
        <h1> <b> Browser Cache Analyzer <br> Scan report [{analysis_date}] </b> </h1>
        <p> <b> Analysis folder: </b> {input_folder} </p>
        <p> <b> Results folder: </b> {output_folder} </p>
        <hr>
        <h2> System info </h2>
        <p> <b> System / Os name: </b> {os_name} </p>
        <p> <b> Release: </b> {release} </p>
        <p> <b> Release version: </b> {release_version} </p>
        <p> <b> Hostname: </b> {hostname} </p>
        <hr>
        <h2> Browser info </h2>
        <p> <b> Browser: </b> {browser} </p>
        <p> <b> Browser version: </b> {browser_version} </p>
        <p> <b> Browser installation path: </b> {browser_inst_path} </p>
        <p> <b> Browser default cache path: </b> {browser_def_path} </p>
        <hr>
        <h2> Cache folder info </h2>
        <p> <b> Cache folder dimension (bytes): </b> {dimension} </p>
        <p> <b> Cache folder elements: </b> {elements} </p>
        <p> <b> Cache folder creation time: </b> {creation_time} </p>
        <p> <b> Cache folder last access: </b> {last_access} </p>
        <hr>
        """.format(
            analysis_date=current_datetime_extended,
            input_folder=self.input_path,
            output_folder=os.path.join(self.output_path, self.scan_main_folder_name),
            os_name=os_name,
            release=os_rel,
            release_version=os_rel_ver,
            hostname=hostname,
            browser=self.browser[0],
            browser_version=self.browser_version[0],
            browser_inst_path=self.browser_inst_path[0],
            browser_def_path=self.browser_def_path[0],
            dimension=folder_info['folder_dimension'],
            elements=folder_info['folder_elements'],
            creation_time=folder_info['folder_creation_time'],
            last_access=folder_info['folder_last_access_time']
        )

        # Chrome index file values
        html_string_report_chrome_index = """
        <h2> index </h2>
        <p> <b> Index : </b> {index_file} </p>
        <p> <b> Signature: </b> {signature} </p>
        <p> <b> Minor version: </b> {minor_version} </p>
        <p> <b> Major version: </b> {major_version} </p>
        <p> <b> Number of entries: </b> {entries} </p>
        <p> <b> Stored data size (bytes): </b> {stored_data} </p>
        <p> <b> Last created f_ file: </b> f_{last_f_file} </p>
        <p> <b> Address table size: </b> {table_size} </p>
        <p> <b> Creation time: </b> {creation_time} </p>
        <p> <b> Index md5: </b> {md5} </p>
        <p> <b> Index sha1: </b> {sha1} </p>
        <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
        <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
        <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
        <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
        <hr>
        """.format(
            index_file=chrome_index_file,
            signature=format(chrome_index_header['signature'], "X"),
            minor_version=chrome_index_header['minor_version'],
            major_version=chrome_index_header['major_version'],
            entries=chrome_index_header['number_of_entries'],
            stored_data=chrome_index_header['stored_data_size'],
            last_f_file=format(chrome_index_header['last_created_file_f'], "06"),
            table_size=chrome_index_header['table_size'],
            creation_time=chrome_index_header['creation_time'],
            md5=chrome_index_info['md5'],
            sha1=chrome_index_info['sha1'],
            dimension=chrome_index_info['file_dimension'],
            os_creation_time=chrome_index_info['creation_time'],
            os_last_modified_time=chrome_index_info['last_modified'],
            os_last_access_time=chrome_index_info['last_access']
        )

        # data_ file info
        html_string_report_chrome_data = ""
        for data_file in os.listdir(self.input_path):
            if "data_" in data_file:
                # Info for current data_ file
                data_num = str(data_file).split("_")[1]
                data_file_path = os.path.join(self.input_path, "data_{num}".format(num=data_num))
                chrome_data_header = data_header.read_data_header(data_to_open=data_file_path)
                chrome_data_info = utils.get_file_info(file_path=data_file_path)
                # data_ file values
                html_string_report_chrome_data += """
                <h2> {data_file} </h2>
                <p> <b> Signature:  </b> {signature} </p>
                <p> <b> Minor version:  </b> {minor_version} </p>
                <p> <b> Major version:  </b> {major_version} </p>
                <p> <b> File number:  </b> {file_number} </p>
                <p> <b> Next file number:  </b> {next_file_number} </p>
                <p> <b> Block size (bytes):  </b> {block_size} </p>
                <p> <b> Number of entries:  </b> {num_entries} </p>
                <p> <b> Max number of entries:  </b> {max_num_entries} </p>
                <p> <b> {data_file} md5:  </b> {md5} </p>
                <p> <b> {data_file} sha1:  </b> {sha1} </p>
                <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
                <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
                <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
                <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
                <hr>
                """.format(
                    data_file=data_file,
                    signature=format(chrome_data_header['signature'], "X"),
                    minor_version=chrome_data_header['minor_version'],
                    major_version=chrome_data_header['major_version'],
                    file_number=chrome_data_header['file_number'],
                    next_file_number=chrome_data_header['next_file_number'],
                    block_size=chrome_data_header['block_size'],
                    num_entries=chrome_data_header['num_entries'],
                    max_num_entries=chrome_data_header['max_num_entries'],
                    md5=chrome_data_info['md5'],
                    sha1=chrome_data_info['sha1'],
                    dimension=chrome_data_info['file_dimension'],
                    os_creation_time=chrome_data_info['creation_time'],
                    os_last_modified_time=chrome_data_info['last_modified'],
                    os_last_access_time=chrome_data_info['last_access']
                )

        # f_ file info
        html_string_report_chrome_f_ = ""
        for sep_file in os.listdir(self.input_path):
            if "f_" in sep_file:
                # # Info for current f_ file
                f_file_path = os.path.join(self.input_path, sep_file)
                chrome_f_info = utils.get_file_info(file_path=f_file_path)
                # f_ file values
                html_string_report_chrome_f_ += """
                <h2> {f_file}  </h2>
                <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
                <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
                <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
                <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
                <p> <b> {f_file} md5: </b> {md5} </p>
                <p> <b> {f_file} sha1: </b> {sha1} </p>
                <hr>
                """.format(
                    f_file=sep_file,
                    dimension=chrome_f_info['file_dimension'],
                    os_creation_time=chrome_f_info['creation_time'],
                    os_last_modified_time=chrome_f_info['last_modified'],
                    os_last_access_time=chrome_f_info['last_access'],
                    md5=chrome_f_info['md5'],
                    sha1=chrome_f_info['sha1']
                )

        html_string_report_close_page = """
        </body >
        </html >
        """

        # Creating index scan report
        with open(scan_report_index, "w") as f_report_index:
            f_report_index.write(
                html_string_report_open_page +
                html_string_report_info +
                html_string_report_chrome_index +
                html_string_report_chrome_data +
                html_string_report_chrome_f_ +
                html_string_report_close_page
            )

        #########################
        # SECTION: SCAN RESULTS #
        #########################
        #
        html_string_results_open_page = """
        <html>
        <head> <title> {scan_date} </title>
        """.format(
            scan_date=current_datetime
        )

        html_string_results_table_style = """
        <style>
        thead {color:green;}
        tbody {color:blue;}
        table, th, td {border: 1px solid black;}
        th {background: white;}
        tr:nth-child(even) {background: white;}
        tr:nth-child(odd) {background: lightgrey;}
        </style>
        </head>
        <body>
        """

        html_string_results_folders = """
        <h1> <b> Browser Cache Analyzer <br> Results report [{analysis_date}] </b> </h1>
        <p> <b> Analysis folder: </b> {input_folder} </p>
        <p> <b> Results folder: </b> {output_folder} </p>
        <hr>
        """.format(
            analysis_date=current_datetime_extended,
            input_folder=self.input_path,
            output_folder=os.path.join(self.output_path, self.scan_main_folder_name)
        )

        html_string_results_entries = """
        <p> <b> Number of entries in index header: </b> {index_entries} </p>
        <p> <b> Number of found entries: </b> {found_entries} </p>
        <hr>
        """.format(
            index_entries=chrome_index_header['number_of_entries'],
            found_entries=len(self.entries_to_export)
        )

        html_string_results_table_header = """
        <table style="width:100%">
        <thead>
        <tr> <th> # </th>
        <th> Key Hash </th>
        <th> Content Type </th>
        <th> Key Url (preview) </th>
        <th> Creation Time </th>
        </tr>
        </thead>
        <tbody>
        """

        html_string_results_table_row = ""
        for idx, entry in enumerate(self.entries_to_export):
            # If "stop export" button is clicked, stopping export
            if self.stop_signal_export.is_set():
                self.stopped_by_user = True
                print "STOP"
                break

            self.update_export_progress_signal.emit(
                idx,
                len(self.entries_to_export)
            )
            # print float((100 * idx)) / float(len(self.entries_to_export))

            entry_name = "{number}{sep}{hash}".format(
                number=format((idx + 1), "02"),
                sep="_",
                hash=entry.key_hash
            )

            html_string_results_table_row += """
            <tr>
            <td> {idx} </td> <td> <a href = ./{file_entry_html} target=_blank> {hash} </td>
            """.format(
                idx=format(idx + 1, "02"),
                file_entry_html=entry_name + ".html",
                hash=entry.key_hash,
            )

            if (entry.data_stream_addresses[0] and
                    isinstance(entry.data_stream_addresses[0].resource_data, dict)):

                if "Content-Type" in entry.data_stream_addresses[0].resource_data:

                    html_string_results_table_row += """
                    <td> {content_type} </td> <td> {key_data} </td> <td> {creation_time} </td>
                    </tr>
                    """.format(
                        content_type=entry.data_stream_addresses[0].resource_data['Content-Type'],
                        key_data=entry.key_data[:75],
                        creation_time=entry.creation_time
                    )
                else:
                    html_string_results_table_row += """
                    <td> Not present </td> <td> {key_data} </td> <td> {creation_time} </td>
                    </tr>
                    """.format(
                        key_data=entry.key_data[:75],
                        creation_time=entry.creation_time
                    )
            else:
                html_string_results_table_row += """
                <td> Unknown </td> <td> {key_data} </td> <td> {creation_time} </td>
                </tr>
                """.format(
                    key_data=entry.key_data[:75],
                    creation_time=entry.creation_time
                )

            # HTML file with entry info
            file_entry = os.path.join(scan_results_path, entry_name)
            with open(file_entry + ".html", "w") as f_entry:
                html_string_file_entry_open_page = """
                <html>
                <head> <title> {entry_name} </title> </head>
                <body>
                """.format(
                    entry_name=entry_name
                )

                html_string_file_entry_container = """
                <h2> Report for entry: {entry} </h2>
                <h3> Container file </h3>
                <p> <b> Container file: </b> {entry_file} </p>
                <p> <b> Container file block dimension: </b> {block_dimension} </p>
                <p> <b> Container file block number: </b> {block_number} </p>
                <p> <b> Container file within offset: </b> {offset} </p>
                <p> <b> Container file md5: </b> {entry_file_md5}  </p>
                <p> <b> Container file sha1: </b> {entry_file_sha1} </p>
                <hr>
                """.format(
                    entry=entry.key_hash,
                    entry_file=entry.entry_file,
                    block_dimension=entry.block_dimension,
                    block_number=entry.block_number,
                    offset=entry.within_file_offset,
                    entry_file_md5=utils.get_file_info(entry.entry_file)['md5'],
                    entry_file_sha1=utils.get_file_info(entry.entry_file)['sha1'],
                )

                html_string_file_entry_values = """
                <h3> Entry values </h3>
                <p> <b> Key hash:  </b> {hash} </p>
                <p> <b> Next entry address: </b> {next_addr} </p>
                <p> <b> Reuse count:  </b> {reuse_count} </p>
                <p> <b> Refetch count: </b> {refetch_count} </b> </p>
                <p> <b> Cache entry state: </b> {entry_state} </p>
                <p> <b> Creation time: </b> {creation_time} </p>
                <p> <b> Key data size:  </b> {key_data_size} </p>
                <p> <b> Long key cache data address: </b> {long_key_addr} </p>
                <p> <b> Cache entry flags:  </b> {flags} </b> <br>
                <p> <b> Key data:  </b> {key_data} </b> </p>
                <hr>
                """.format(
                    hash=entry.key_hash,
                    next_addr=entry.next_entry_address,
                    reuse_count=entry.reuse_count,
                    refetch_count=entry.refetch_count,
                    entry_state=entry.entry_state,
                    creation_time=entry.creation_time,
                    key_data_size=entry.key_data_size,
                    long_key_addr=entry.long_key_data_address,
                    flags=entry.cache_entry_flags,
                    key_data=entry.key_data
                )

                html_string_file_http_header = ""
                # Checking http headers
                for str_add, item in enumerate(entry.data_stream_addresses):
                    file_entry_data = "".join((file_entry, "-data{num}".format(num=str_add)))
                    # Header position in data stream addresses
                    if str_add == 0:

                        header_dimension = 8192
                        resource_file = item.resource_file
                        block_dimension = item.block_dimension
                        block_number = item.block_number
                        resource_size = item.resource_size
                        resource_offset = header_dimension + (block_dimension * block_number)

                        with open(resource_file, "rb") as f_resource:
                            f_resource.seek(resource_offset)
                            resource_data = f_resource.read(resource_size)
                            with open(file_entry_data, "wb") as f_entry_data:
                                f_entry_data.write(resource_data)

                                # Header dictionary
                        if item and isinstance(item.resource_data, dict):
                            html_string_file_http_header += """
                            <h3> Header </h3>
                            """
                            for key, key_value in item.resource_data.iteritems():
                                html_string_file_http_header += """
                                <p> <b> {key}: </b> {key_value} </p>
                                """.format(
                                    key=key,
                                    key_value=key_value
                                )
                            html_string_file_http_header += """
                            <hr>
                            """

                            # If "image" in Header keys
                            for key, key_value in item.resource_data.iteritems():
                                if key == "Content-Type" and "image" in key_value:
                                    html_string_file_http_header += """
                                    <h3> Image </h3>
                                    <p> <img src="{image_src}" alt="No image available" /> </p>
                                    """.format(
                                        image_src=file_entry_data,
                                    )

                    elif str_add != 0:
                        if item:
                            if not item.is_http_header or item.is_http_header == "Unknown":

                                # Key data not in separate file
                                if item.file_type != "000":
                                    with open(file_entry_data, "wb") as f_entry_data:
                                        # Resource value
                                        f_entry_data.write(str(item.resource_data))

                                # Key data in separate file
                                else:
                                    shutil.copy(item.resource_file, file_entry_data)

                html_string_file_entry_close_page = """
                </body>
                </html>
                """

                f_entry.write(html_string_file_entry_open_page +
                              html_string_file_entry_container +
                              html_string_file_entry_values +
                              html_string_file_http_header +
                              html_string_file_entry_close_page
                              )

        html_string_results_close_page = """
        </tbody>
        </table>
        </body>
        </html>
        """

        # Creating index results report
        with open(scan_results_index, "w") as f_scan_index:
            f_scan_index.write(
                html_string_results_open_page +
                html_string_results_table_style +
                html_string_results_folders +
                html_string_results_entries +
                html_string_results_table_header +
                html_string_results_table_row +
                html_string_results_close_page
            )

        print "finito export"
        # webbrowser.open(scan_report_index)
        # webbrowser.open(scan_results_index)
