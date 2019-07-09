# Finnish Word Embeddings

**finnish-word-embeddings** aims to collect [word embeddings](https://en.wikipedia.org/wiki/Word_embedding) for [Finnish language](https://en.wikipedia.org/wiki/Finnish_language) in one place. This repository contains both word embeddings trained by the author, but also links to Finnish word embeddings provided by others.

## List of available embeddings
|   Source																|   Model		|   Dimension	|  	Trained on								|	Download link 	|
|---																	|---			|---			|---										|---			  	|
|   [Facebook](https://fasttext.cc/docs/en/crawl-vectors.html)			|   FastText	|	300			| 	Wikipedia and CommonCrawl				|		[Binary](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.fi.300.bin.gz) / [Text](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.fi.300.vec.gz) |
|   [Facebook](https://fasttext.cc/docs/en/pretrained-vectors.html)		|   FastText	|	300			| 	Wikipedia								|		[Binary + Text](https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.fi.zip) / [Text](https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.fi.vec)	|
|   [Turku NLP](https://turkunlp.org/finnish_nlp.html)					|  	Word2Vec	|	Unknown 	|   Finnish Internet Parsebank (4B tokens)	|	[Binary](http://dl.turkunlp.org/finnish-embeddings/finnish_4B_parsebank_skgram.bin)				|
|   [Turku NLP](https://turkunlp.org/finnish_nlp.html)					|  	Word2Vec	|	Unknown 	|   Suomi24									|	[Binary](http://dl.turkunlp.org/finnish-embeddings/finnish_s24_skgram.bin)				|
|   [Turku NLP](https://turkunlp.org/finnish_nlp.html)					|  	Word2Vec	|	Unknown 	|   Suomi24 with lemmatization				|	[Binary](http://dl.turkunlp.org/finnish-embeddings/finnish_s24_skgram_lemmas.bin)				|
|   This repository														|   			|   			|   										|					|


## Example usage of word embeddings


## Training your own word embeddings

This repository contains the code used for gathering data from the web and training custom word embeddings.

## Acknowledgements and references
* 
		
---
Jesse Myrberg (jesse.myrberg@gmail.com)