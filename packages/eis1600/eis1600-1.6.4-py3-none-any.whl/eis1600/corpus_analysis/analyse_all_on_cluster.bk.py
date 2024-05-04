from typing import Optional
from sys import argv, exit
from argparse import ArgumentParser, RawDescriptionHelpFormatter, ArgumentTypeError
from functools import partial
from pathlib import Path
from logging import ERROR, Formatter, INFO
from time import process_time, time
from random import shuffle

import os #FIXME

import jsonpickle
from tqdm import tqdm
from p_tqdm import p_uimap

from torch import cuda

from eis1600.corpus_analysis.miu_methods import analyse_miu
from eis1600.corpus_analysis.text_methods import get_text_as_list_of_mius
from eis1600.helper.logging import setup_persistent_logger
from eis1600.repositories.repo import JSON_REPO, TEXT_REPO, get_ready_and_double_checked_files


def parse_range(arg: str) -> tuple[int, int | None]:
    try:
        i, j = arg.split(",")
        i = int(i) - 1 if i else 0
        j = int(j) if j else None
        return i, j
    except ValueError:
        raise ArgumentTypeError("range must be i,j with both i and j being integers")


def routine_per_text(
        infile: str,
        parallel: Optional[bool] = False,
        force: Optional[bool] = False,
        debug: Optional[bool] = False,
    ):
    """Entry into analysis routine per text.

    Each text is disassembled into the list of MIUs. Analysis is applied to each MIU. Writes a JSON file containing
    the list of MIUs with their analysis results.
    :param ste infile: EIS1600 text which is analysed.
    :param bool parallel: Parallel flag for parallel processing, otherwise serial processing.
    :param bool force: Do processing even though file already exists.
    :param bool debug: Debug flag for more console messages.
    """
    out_path = infile.replace(TEXT_REPO, JSON_REPO)
    out_path = out_path.replace('.EIS1600', '.json')

    # do not process file is it's already generated
    if Path(out_path).exists() and not force:
        return

    meta_data_header, mius_list = get_text_as_list_of_mius(infile)

    res = []
    error = ''
    if parallel:
        res += p_uimap(partial(analyse_miu, debug=debug), mius_list)
    else:
        for idx, tup in tqdm(list(enumerate(mius_list))):
            try:
                res.append(analyse_miu(tup, debug))
            except Exception as e:
                uid, miu_as_text, analyse_flag = tup
                error += f'{uid}\n{e}\n\n\n'

    dir_path = '/'.join(out_path.split('/')[:-1])
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    with open(out_path, 'w', encoding='utf-8') as fh:
        jsonpickle.set_encoder_options('json', indent=4, ensure_ascii=False)
        json_str = jsonpickle.encode(res, unpicklable=False)
        fh.write(json_str)

    if error:
        raise ValueError(error)


def main():
    arg_parser = ArgumentParser(
        prog=argv[0], formatter_class=RawDescriptionHelpFormatter,
        description='''Script to parse whole corpus to annotated MIUs.'''
    )
    arg_parser.add_argument('-D', '--debug', action='store_true')
    arg_parser.add_argument('-P', '--parallel', action='store_true')
    arg_parser.add_argument(
        '--range',
        metavar="ini,end",
        type=parse_range,
        help='process file range [i,j] (both are optional)'
    )
    arg_parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="randomise list of files"
    )
    arg_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="process file regardless if it exist and overwrite it"
    )

    args = arg_parser.parse_args()
    debug = args.debug
    parallel = args.parallel
    force = args.force

    print(f'GPU available: {cuda.is_available()}')

    st = time()
    stp = process_time()

    # Retrieve all double-checked texts
    files_ready, files_double_checked = get_ready_and_double_checked_files()
    infiles = files_ready + files_double_checked

    if not infiles:
        print('There are no EIS1600 files to process')
        exit()

    logger = setup_persistent_logger('analyse_all_on_cluster', 'analyse_all_on_cluster.log', INFO)

    if args.range:
        infiles = infiles[args.range[0]:args.range[1]]

    infiles_indexes = list(range(len(infiles)))

    #infiles_indexes = sorted(infiles_indexes, key=lambda f: os.path.getsize(infiles[f]), reverse=True) #FIXME sort by longest to smallest
    #for i in infiles_indexes: #FIXME
    #    num = f"[{i+1}]" #FIXME
    #    infile = infiles[i]  # FIXME
    #    size = os.path.getsize(infile) #FIXME
    #    mb = size >> 20 #FIXME
    #    #if "part" in infile: #FIXME
    #    print(f"{num:<6} {size:<8} {mb:<2} {infile}") #FIXME
    #print("Total =", len(infiles_indexes)) #FIXME wtf !!!!! no tiene sentido
    #import sys #FIXME
    #sys.exit() #FIXME
    #infiles_indexes = sorted(infiles_indexes, key=lambda f: os.path.getsize(infiles[f]), reverse=True)[:1] #FIXME biggest doc
    #infiles_indexes = sorted(infiles_indexes, key=lambda f: os.path.getsize(infiles[f]))[:1]  # FIXME  smallest doc !!

    if args.random:
        shuffle(infiles_indexes)

    for i in tqdm(infiles_indexes):
        infile = infiles[i]
        print(f"[{i+1}] {infile}")
        try:
            routine_per_text(infile, parallel, force, debug)
        except ValueError as e:
            logger.log(ERROR, f'{infile}\n{e}')

    et = time()
    etp = process_time()

    print('Done')
    print(f'Processing time: {etp - stp} seconds')
    print(f'Execution time: {et - st} seconds')
