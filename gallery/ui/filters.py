import arrow
import os
import mimetypes

def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()

def file_type(key):
    file_info = os.path.splitext(key)
    file_extension = file_info[1]
    return mimetypes.types_map[file_extension]
    # try:
    #     return mimetypes.types_map[file_extension]
    # except KeyError() as e:
    #     return 'Unknown'