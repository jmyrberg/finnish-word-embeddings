"""Module for updating all word embeddings with the latest crawled data."""


from preprocess import preprocess_all_files
from train import create_all_embeddings


def main():
    preprocess_all_files(
        in_filedir='./data/feed/',
        out_filepath='./data/processed/all.sl',
        lines_per_chunk=30000,
        create_uncased=True,
        min_sent_len=5,
        tokenizer='tweet',
        n_jobs=3
    )
    create_all_embeddings(
        sentlines_dir='./data/processed',
        out_dir='./data/embeddings'
    )
    

if __name__ == '__main__':
    main()