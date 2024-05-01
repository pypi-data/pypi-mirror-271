<h1 align="center" id="title">Studcamp Yandex x HSE</h1>

<h2 align="center" id="title">Text Tagging</h2>

<h3 align='left'> My team and I, within machine learning studcamp by Yandex and HSE, developed a whole module for "Text Tagging" problem, in terms of keywords extraction. </h3>

<h3 align='left'> We had a big research. We've tried several extractive and abstractive methods. We will discuss it further.</h3>

<h2>🚀 Demo</h2>

![Streamlit Demo](./materials/streamlit-Info-2024-04-30-15-04-49.gif)

<h2>🧪 Preprocessing</h2>

*   **Embedder Module:** FastText/RuBert embeddings realisation
*   **Normalizer Modlule:**  Nouns extraction + Punctuation removal + Stopwords removal (For extractive models)
*   **Ranker Module:** Module which ranks the most significant words by distance in embedding space (max_distance_ranker) and by cosine similarity with text embeddings (text_sim_ranker)
*   **Summarizator Module:** Module which summarizes the text with MBart model

<h2>🤖 Models</h2>

### Exctractive models
*   **RakeBasedTagger:** This is a model which based on a well-known Rake algorithm, that extract meaningful words from text. It's very fast and can be used online. After extracting meaningful words, we should normalize such words and performing filtering with taking only top_n words with the largest distance between query word and other meaningful words. This algorithm supposes that keywords should be as far as possible from each other to represent different domains of the text.
*   **BartBasedTagger:** This is a rubert-based model which makes an assumption that we could find the most significat words to our text as such with the best cosine similarity. During the pipeline, firstly we need to summarize our text with MBart model, then we should extract the most significant words with cosine similarity for text embedding with each word embedding of the text via rubert represenation. This model is very slow and can be used offline, as we need to summarize text before main processing.
*   **AttentionBasedTagger:** This is a very interesting model. We assumed that all the algorithms above couldn't catch bigram keywords. So, we decided to use attention mechanism. Let's compute attention activation for every pair of tokens. The biggest activation means, that such words are meaningful to each other. The other problem was that Mbart uses bpe tokenizer and we should perform some post-processing to construct interpretable keywords.
*   **ClusterizationBasedTagger:** Experimental extractitve model. We used DBSCAN on embeddings of words from normalized text to get clusters of words with similar meaning. Each cluster centroid embedding is a potential keyword. So, we can convert it's embedding to the nearest fasttext word embedding.

### Abstractive models
*   **RuT5Tagger:** Model that was trained on an aggregated dataset from different sources like 'Живой журнал', 'Пикабу' etc. It needs to be mentioned that this model is abstractive, so it can generate new keywords that are not present in the text. Moreover, such model need to be trained on a big dataset further to be able to give good results.

<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Online model: Rake Based Model with 10-20 it/sec (The fastest)
*   Offline models: Bart based model with summarisation or attention. 1-5 it/sec (The slowest)

<h2>🛠️ Installation Steps:</h2>

#### Please, use python@3.10

<p>1. Installation</p>

```
pip install studcamp-yandex-hse
```

<p>2. Download russian FastText embeddings and RuT5 weights with the links below and paste it at the same level as your source .py file</p>

```
FastText embeddings: https://fasttext.cc/docs/en/crawl-vectors.html
Weights: https://drive.google.com/file/d/1aqVtoNRX3xDokthxuBNFwfcXQfkKeAMa/view?usp=sharing
```

<p>3. Import</p>

```
from studcamp_yandex_hse.models import RakeBasedTagger, BartBasedTagger, AttentionBasedTagger, ClusterizationBasedTagger, RuT5Tagger
from studcamp_yandex_hse.processing.embedder import FastTextEmbedder
```

<p>4. Init FastTextEmbedder (We need to pass the instance as argument for Rake and Clusterized models)</p>

```
ft_emb_model = FastTextEmbedder()
```

<p>5. Init Model</p>

```
tagger = RakeBasedTagger(ft_emb_model)
```

<p>6. Get tags</p>

```
text = '...'
top_n = 5

tagger.extract(some_text, top_n)
```
