"""Module for preprocessing of crawled data."""


from utils import get_logger
logger = get_logger()

import gc
import glob
import os
import re
import time
import string
import ujson as json

from itertools import zip_longest

import nltk
import numpy as np
import pandas as pd

from joblib import Parallel, delayed


def grouper(iterable, n, fillvalue=None):
    """Return iterable in chunks of certain length.
    
    Args:
        iterable (iterable): Iterable to return chunks from.
        n (int): Length of a chunk.
        fillvalue (any, optional): Value to fill when iterable has been consumed
            entirely. Defaults to None.
    
    Returns:
        iterable: Iterable of length n.
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def preprocess_lines(lines, tokenizer, sent_tokenizer, min_sent_len=5):
    """Preprocess given JSON lines.
    
    Args:
        lines (list): List of strings (JSON lines).
        tokenizer (object): Word tokenizer with 'tokenize' -method.
        sent_tokenizer (object): Sentence tokenizer with 'tokenize' -method.
        min_sent_len (int, optional): Minimum number of tokens to be considered
            as a sentence. Defaults to 5.
    
    Returns:
        list: List of preprocessed sentences as strings.
    """
    contents = [c for js in json.loads('[' + ','.join(lines) + ']')
                for c in js['content']]
    
    filter_re = re.compile(r'[^\w\s]')
    url_re = re.compile(r'\w+:\/\/\S*')
    
    sents = []
    for doc in contents:
        
        for sent in sent_tokenizer.tokenize(doc):
            sent_tokens = []
            
            # Remove URLs
            sent = url_re.sub('<URL>', sent)
            
            # Tokenization
            tokens = tokenizer.tokenize(sent)

            # Cleaning up
            for token in tokens:
                
                # Normal tokens
                normal_chars = filter_re.sub('', token)
                n_token = len(token)
                n_normal_chars = len(normal_chars)
                pct_normal_chars = n_normal_chars / n_token
                if n_normal_chars > 0 and pct_normal_chars > 0.75:
                    sent_tokens.append(token)
                    continue
                    
                # Emojis
                other_chars = filter_re.findall(token)
                only_one_other = len(other_chars) == 1
                others_in_punct = any([c in string.punctuation 
                                       for c in other_chars])
                if only_one_other and not others_in_punct:
                    sent_tokens.append(token)
            
            # Add to sentences
            if len(sent_tokens) >= min_sent_len:
                clean_sent = ' '.join(sent_tokens)
                sents.append(clean_sent)
    return sents


def parallel_preprocess_lines(lines, tokenizer, sent_tokenizer,
                              n_jobs=3, min_sent_len=5):
    """Parallel preprocessing of lines.
    
    Args:
        lines (list): List of strings that are crawled lines and not in
            JSON format yet.
        tokenizer (object): Word tokenizer with 'tokenize' -method.
        sent_tokenizer (object): Sentence tokenizer with 'tokenize' -method.
        n_jobs (int, optional): Number of parallel workers to use. Defaults to
            3.
        min_sent_len (int, optional): Minimum number of tokens to be considered
            as a sentence. Defaults to 5.
            
    Returns:
        List of unique sentences in an array.
    """
    n = int(np.ceil(len(lines) / n_jobs))
    job_lines = [lines[i:i + n] for i in range(0, len(lines), n)]
    sent_lists = Parallel(n_jobs=n_jobs)(
        delayed(preprocess_lines)(
            lines=lines,
            tokenizer=tokenizer,
            sent_tokenizer=sent_tokenizer,
            min_sent_len=min_sent_len
        )
        for lines in job_lines
    )
    sents = [sent for sent_list in sent_lists for sent in sent_list]
    return pd.unique(sents)
      

def preprocess_file(filepath, tokenizer, sent_tokenizer,
                 out_filepath='./data/processed/test.sl',
                 mode='a', lines_per_chunk=30000, min_sent_len=5, n_jobs=3):
    """Preprocess single crawled JSON line file in chunks.
    
    Args:
        filepath (str): Path to JSON line file to be preprocessed.
        tokenizer (object): Word tokenizer with 'tokenize' -method.
        sent_tokenizer (object): Sentence tokenizer with 'tokenize' -method.
        out_filepath (str, optional): Filepath of the output sentence lines.
            Defaults to './data/processed/test.sl'.
        mode (str, optional): Mode to open output file with. Defaults to 'a'.
        lines_per_chunk (int, optional): Number of JSON lines to be processed
            in one chunk. Defaults to 30000.
        min_sent_len (int, optional): Minimum number of tokens to be considered
            as a sentence. Defaults to 5.
        n_jobs (int, optional): Number of parallel workers to use. Defaults to 
            3.
    """
    with open(filepath, 'r', encoding='utf8') as f:
        logger.info('Reading number of lines in the file...')
        n_total_lines = sum(1 for _ in f)
        f.seek(0)
        
        with open(out_filepath, mode=mode, encoding='utf8') as fout:
            it = grouper(f, lines_per_chunk)
            for i,lines in enumerate(it):
                start_time = time.perf_counter()
                end_line = min((i + 1) * lines_per_chunk, n_total_lines) / 1e3
                logger.info(f'Lines {i * lines_per_chunk / 1e3:.0f}'
                            f' - {end_line:.0f}k '
                            f'/ {n_total_lines / 1e3:.0f}k')
                
                sents = parallel_preprocess_lines(
                    [l for l in lines if l],
                    tokenizer=tokenizer,
                    sent_tokenizer=sent_tokenizer,
                    n_jobs=n_jobs,
                    min_sent_len=min_sent_len
                )
                
                logger.info(f'Writing {len(sents)} sentences...')
                fout.write('\n'.join(sents))
                
                time_passed = time.perf_counter() - start_time
                logger.info(f'Chunk done in {time_passed:.0f} seconds!')
                gc.collect()


def preprocess_all_files(in_filedir='./data/feed/',
                         out_filepath='./data/processed/all2.sl',
                         lines_per_chunk=30000,
                         create_uncased=True,
                         min_sent_len=5,
                         tokenizer='tweet',
                         n_jobs=3):
    """Preprocess all crawled JSON line files in a folder.
    
    Args:
        in_filedir (str, optional): Path to directory of JSON line files to be
            preprocessed. Defaults to './data/feed/'.
        out_filepath (str, optional): Filepath of the output sentence lines.
            Defaults to './data/processed/all.sl'.
        lines_per_chunk (int, optional): Number of JSON lines to be processed
            in one chunk. Defaults to 30000.
        create_uncased (bool, optional): Whether to create uncased version of
            the sentences or not. The name will be same as out_filepath + 
            '_uncased.sl'. Defaults to True.
        min_sent_len (int, optional): Minimum number of tokens to be considered
            as a sentence. Defaults to 5.
        tokenizer (str, optional): Word tokenizer to use. Should be in 
            ['tweet']. Defaults to 'tweet'.
        n_jobs (int, optional): Number of parallel workers to use. Defaults to 
            3.
    
    Raises:
        ValueError: If tokenizer name not in the list of allowed tokenizers.
    """
    start_time = time.perf_counter()
    
    # Solve paths
    filepaths = [os.path.abspath(p) for p in glob.glob(in_filedir + '*.jl')]
    
    out_filepath = os.path.abspath(out_filepath)
    out_dir = os.path.dirname(out_filepath)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        logger.warn(f'Created directory in {out_dir}')
    
    # Tokenizers
    if tokenizer.lower().strip() == 'tweet':
        from nltk.tokenize import TweetTokenizer
        tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True, 
                                   preserve_case=True)
    else:
        raise ValueError('Currently only "tweet" tokenizer is supported!')
    sent_tokenizer = nltk.data.load('tokenizers/punkt/finnish.pickle')
    
    # Preprocessing
    for i,path in enumerate(filepaths):
        logger.info(f'Processing file "{path}" '
                    f'({i + 1} / {len(filepaths)})')
        preprocess_file(
            filepath=path,
            mode='w' if i == 0 else 'a',
            lines_per_chunk=lines_per_chunk,
            out_filepath=out_filepath, min_sent_len=min_sent_len,
            tokenizer=tokenizer,
            sent_tokenizer=sent_tokenizer,
            n_jobs=n_jobs
        )
        
    # Uncased version of the sentence lines
    if create_uncased:
        uncased_filepath = os.path.join(
            os.path.dirname(out_filepath),
            os.path.splitext(out_filepath)[0] + '.uncased.sl')
        logger.info(f'Creating uncased into "{uncased_filepath}"...')
        with open(out_filepath, 'r', encoding='utf8') as f:
            with open(uncased_filepath, 'w', encoding='utf8') as fout:
                for line in f:
                    fout.write(line.lower())
                    
    logger.info(f'All done in {time.perf_counter() - start_time:.0f} seconds!')
    

#if __name__ == '__main__':
#    preprocess_all_files()