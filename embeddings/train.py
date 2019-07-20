"""Module for training word embeddings."""


from utils import get_logger
logger = get_logger()

import glob
import gzip
import os
import shutil
import time

from gensim.models import Word2Vec,FastText
from gensim.models.word2vec import LineSentence


def get_out_filepaths(in_filepath, out_dir, model_name, size, n_tokens):
    """Get output filepaths for word embeddings based on model parameters.
    
    Args:
        in_filepath (str): Filepath of input sentence lines file.
        out_dir (str): Directory to save word embeddings into.
        model_name (str): Name of the word embeddings model.
        size (int): Word embeddings vector dimension.
        n_tokens (int): Number of tokens that the model was trained on.
    
    Returns:
        tuple: Two-element tuple with output path for binary and text files.
    """
    in_filename = os.path.splitext(os.path.basename(in_filepath))[0]
    if model_name:
        in_filename = (f'{model_name}.fi.{in_filename}'
                       f'.{n_tokens / 1e6:.0f}M.{size}d')
    out_filepath = os.path.abspath(os.path.join(out_dir, in_filename))
    return f'{out_filepath}.bin',f'{out_filepath}.vec'


def gzip_file(filepath, remove_original=True):
    """Gzip compress given file.
    
    Args:
        filepath (str): Path to file to be compressed.
        remove_original (bool, optional): Whether to remove the original file
            or not. Defaults to True.
    """
    with open(filepath, 'rb') as f_in:
        with gzip.open(f'{filepath}.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    if remove_original:
        os.remove(filepath)


def save_word_vectors(sentlines_path, out_dir, model,
                      save_vec=False, compress=True):
    """Save word vectors of a gensim model into a directory.
    
    Args:
        sentlines_path (str): Filepath of input sentence lines file.
        out_dir (str): Directory to save word embeddings into.
        model (gensim.models.*): Trained gensim model.
        save_vec (bool, optional): Whether to save vectors in text format.
            Defaults to False.
        compress (bool, optional): Whether to Gzip the output or not. Defaults
            to True.
    """
    model_name = model.__class__.__name__.lower()
    n_tokens = model.corpus_total_words
    size = model.vector_size
    (out_binary_filepath,
     out_text_filepath) = get_out_filepaths(sentlines_path, out_dir,
                                            model_name, size, n_tokens)
    model.wv.save_word2vec_format(out_binary_filepath, binary=True)
    if save_vec:
        model.wv.save_word2vec_format(out_text_filepath, binary=False)

    if compress:
        gzip_file(out_binary_filepath)
        if save_vec:
            gzip_file(out_text_filepath)


def create_word2vec_embeddings(sentlines_path, out_dir, size=300):
    """Train Word2Vec word embeddings.
    
    Args:
        sentlines_path (str): Filepath of input sentence lines file.
        out_dir (str): Directory to save word embeddings into.
        size (int, optional): Word embeddings vector dimension. Defaults to 100.
    """
    sentences = LineSentence(sentlines_path)
    w2v = Word2Vec(
        window=5,
        size=size,
        min_count=5,
        max_vocab_size=None,
        workers=4
    )
    w2v.build_vocab(sentences, progress_per=1e6)
    w2v.train(
        sentences,
        total_examples=w2v.corpus_count,
        epochs=w2v.epochs,
        queue_factor=2
    )
    save_word_vectors(sentlines_path, out_dir, w2v)
    

def create_fasttext_embeddings(sentlines_path, out_dir, size=300):
    """Train FastText word embeddings.
    
    Args:
        sentlines_path (str): Filepath of input sentence lines file.
        out_dir (str): Directory to save word embeddings into.
        size (int, optional): Word embeddings vector dimension. Defaults to 100.
    """
    sentences = LineSentence(sentlines_path)
    ft = FastText(
        window=5,
        size=size,
        min_count=5,
        max_vocab_size=None,
        workers=4
    )
    ft.build_vocab(sentences, progress_per=1e6)
    ft.train(
        sentences,
        total_examples=ft.corpus_count,
        epochs=ft.epochs,
        queue_factor=2
    )
    save_word_vectors(sentlines_path, out_dir, ft)


def create_all_embeddings(sentlines_dir='./data/processed',
                          out_dir='./data/embeddings'):
    """Train all word embeddings based on sentence line files in a directory.
    
    Args:
        sentlines_dir (str, optional): Directory that contains sentence lines
            files to train models on. Defaults to './data/processed'.
        out_dir (str, optional): Directory to save word embeddings into.
            Defaults to './data/embeddings'.
    """
    start_time = time.perf_counter()
    
    # Filepaths
    sentline_filepaths = glob.glob(os.path.join(sentlines_dir, '*.sl'))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        logger.warning(f'Created directory in "{out_dir}"')

    # Train word embeddings
    for filepath in sentline_filepaths:
        logger.info(f'Creating embeddings for sentlines {filepath}...')

        # 300d
        create_word2vec_embeddings(filepath, out_dir, size=300)
        create_fasttext_embeddings(filepath, out_dir, size=300)
        
    logger.info(f'All done in {time.perf_counter() - start_time:.0f} seconds!')


#if __name__ == '__main__':
#    create_all_embeddings()
