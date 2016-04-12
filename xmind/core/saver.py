#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.saver
    ~~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""
import os

__author__ = "aiqi@xmind.net <Woody Ai>"

import codecs

from . import const
from .. import utils


class WorkbookSaver(object):
    def __init__(self, workbook):
        """ Save `WorkbookDocument` as XMind file.

        :param workbook: `WorkbookDocument` object

        """
        self._workbook = workbook

    def _get_content(self):
        content_path = utils.join_path(utils.temp_dir(), const.CONTENT_XML)

        with codecs.open(content_path, "w", encoding="utf-8") as f:
            self._workbook.output(f)

        return content_path

    def save(self, path=None):
        """
        Save the workbook to the given path. If the path is not given, then
        will save to the path set in workbook.
        """
        path = path or self._workbook.get_path()

        if not path:
            raise Exception("Please specify a filename for the XMind file")

        path = utils.get_abs_path(path)

        file_name, ext = utils.split_ext(path)

        if ext != const.XMIND_EXT:
            raise Exception("XMind filenames require a '%s' extension" % const.XMIND_EXT)

        content = self._get_content()

        f=utils.compress(path)
        f.write(content, const.CONTENT_XML)

    def _get_reference(self, old_path):
        reference_dir = utils.temp_dir()

        old_file_name, old_ext = utils.split_ext(old_path)

        if old_ext != const.XMIND_EXT:
            raise Exception("XMind filenames require a '%s' extension" % const.XMIND_EXT)

        myzip = utils.extract(old_path)
        with myzip as input_stream:
            for name in input_stream.namelist():
                print(name)
                if name == const.CONTENT_XML:
                    continue
                if const.REVISIONS_DIR in name:
                    continue

                target_file = utils.get_abs_path(utils.join_path(reference_dir,name))
                if not os.path.exists(os.path.dirname(target_file)):
                    os.makedirs(os.path.dirname(target_file))
                f_handle=open(target_file,"xb")
                f_handle.write(myzip.read(name))
                f_handle.close()

        return reference_dir

    def save_all(self, path=None):
        """
        Save the workbook to the given path with all references except Revisions for saving space.
        If the path is not given, then will save to the path set in workbook.
        """
        old_path = self._workbook.get_path()
        path = path or self._workbook.get_path()

        if not path:
            raise Exception("Please specify a filename for the XMind file")

        path = utils.get_abs_path(path)
        old_path = utils.get_abs_path(old_path)

        file_name, ext = utils.split_ext(path)
        old_file_name, old_ext = utils.split_ext(old_path)

        if ext != const.XMIND_EXT:
            raise Exception("XMind filenames require a '%s' extension" % const.XMIND_EXT)

        if old_ext != const.XMIND_EXT:
            raise Exception("XMind filenames require a '%s' extension" % const.XMIND_EXT)

        content = self._get_content()
        reference_dir = self._get_reference(old_path)

        f = utils.compress(path)
        f.write(content, const.CONTENT_XML)

        len = reference_dir.__len__()
        for dirpath, dirnames, filenames in os.walk(reference_dir):
            for filename in filenames:
                f.write(utils.join_path(dirpath, filename), utils.join_path(dirpath[len+1:]+os.sep, filename))
        f.close()

def main():
    pass

if __name__ == "__main__":
    main()
