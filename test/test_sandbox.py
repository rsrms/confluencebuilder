# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2019 by the contributors (see AUTHORS file).
    :license: BSD-2-Clause, see LICENSE for details.
"""
from sphinxcontrib_confluencebuilder_util import ConfluenceTestUtil as _
from sphinxcontrib.confluencebuilder.exceptions import ConfluenceBadApiError
from sphinxcontrib.confluencebuilder.publisher import ConfluencePublisher
import argparse
import os
import sys

def process_sandbox(builder=None):
    test_dir = os.path.dirname(os.path.realpath(__file__))
    sandbox_dir = os.path.join(test_dir, 'sandbox')

    doc_dir, doctree_dir = _.prepareDirectories('sandbox-test')
    _.buildSphinx(sandbox_dir, doc_dir, doctree_dir, builder=builder,
        relax=True)

def process_raw_upload():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    sandbox_dir = os.path.join(test_dir, 'sandbox')
    raw_file = os.path.join(sandbox_dir, 'raw.conf')

    if not os.path.exists(raw_file):
        print('[sandbox] missing file', raw_file)
        return

    doc_dir, doctree_dir = _.prepareDirectories('sandbox-test')
    with _.prepareSphinx(sandbox_dir, doc_dir, doctree_dir, relax=True) as app:
        publisher = ConfluencePublisher()
        publisher.init(app.config)
        publisher.connect()

        while True:
            with open(raw_file, 'r') as f:
                data = f.read()

            print('[sandbox] publishing page...')
            try:
                publisher.storePage('raw', data)
            except ConfluenceBadApiError as ex:
                print('[sandbox] failed to publish content:', ex)

            print('[sandbox] any key to retry; q to quit')
            if input().lower() == 'q':
                break

def main():
    _.enableVerbose()

    parser = argparse.ArgumentParser(prog=__name__,
        description='Atlassian Confluence Sphinx Extension Sandbox')
    parser.add_argument('--builder', '-b')
    parser.add_argument('--raw-upload', '-R', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')

    args, ___ = parser.parse_known_args(sys.argv[1:])
    parser.parse_args()

    if args.verbose:
        if 'SPHINX_VERBOSITY' not in os.environ:
            os.environ['SPHINX_VERBOSITY'] = '2'

    if args.raw_upload:
        print('[sandbox] raw-upload test')
        process_raw_upload()
    else:
        print('[sandbox] documentation test')
        process_sandbox(args.builder)

    return 0

if __name__ == '__main__':
    sys.exit(main())
