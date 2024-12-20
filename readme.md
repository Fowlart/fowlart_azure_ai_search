# Application: Intelligent Document Summarization and Search

## Core Functionality:

Users upload documents (**text files**).

Python code processes the documents:
- ~~Extracts text using plain file reading~~. 
- ~~Cleans the text (remove noise, punctuation, etc.).~~
- ~~Extract key phrases~~ and entities (**Azure AI Language services**).
- ~~Perform language detection~~ (**Azure AI Language services**).


- **How can data in text files be searched more effectively?**.
  - _custom content vectorization ?_
  - semantic search (**AI Search**) ?
  - question answering (**AI Search**) ?
  - custom text classification (**AI Search**) ?
  - custom NER (**AI Search**) ?

  
- Faceting options (e.g., document type, sentiment, language, entities)(**AI Search**).

- ~~Users perform keyword searches. Azure AI Search retrieves relevant documents~~.

- The application presents search results with summaries, ~~key phrases, and relevant metadata (facets)~~. 

- Implement integration with a blob storage for generating URLs for download

## Enhancements (Optional):

- Create a user-friendly web or desktop interface using libraries like Flask or Streamlit.
- Advanced Search: Implement more advanced search features (e.g., fuzzy search, semantic search).
- Machine Learning Integration: Train a custom machine learning model for document classification or summarization.
- Make the code reusable and environment-independent