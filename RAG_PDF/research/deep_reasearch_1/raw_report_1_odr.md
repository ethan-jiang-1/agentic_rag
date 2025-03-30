Recent RAG System Designs for PDF-based Knowledge Bases (June 2024 – Present)
Retrieval-Augmented Generation (RAG) pipelines that handle PDF documents have evolved rapidly since mid-2024. Below we survey several practical, engineering-focused RAG system designs (June 2024 onward) that emphasize robust PDF chunking, hybrid/structured retrieval, and real-world production considerations. Each entry includes the source’s title, author/organization, publication date, a summary of key engineering takeaways, PDF chunking & retrieval strategies, system pipeline details, and a reference URL.
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain
Author/Org: Brian McGough (Medium)
Date: July 18, 2024
Summary: This Medium article provides a step-by-step guide to constructing a RAG pipeline for searching information in PDF documents using LangChain​
MEDIUM.COM
​
MEDIUM.COM
. It addresses common production challenges (slow processing, high costs, unpredictable outputs) and emphasizes evaluation and iteration (using LangSmith) to fine-tune the pipeline for accuracy and reliability.
PDF Chunking & Retrieval: The author highlights the importance of chunking PDF text into manageable, overlapping segments for effective retrieval​
MEDIUM.COM
. Using LangChain’s RecursiveCharacterTextSplitter, the PDF is split into ~300-character chunks with 50-character overlaps, preserving sentence/paragraph boundaries​
MEDIUM.COM
. This overlap helps maintain context continuity across chunks. The chunks are then embedded using OpenAI embeddings and indexed in a Chroma vector database​
MEDIUM.COM
. Such careful chunk sizing and overlap tuning prevent context loss and improve retrieval relevance.
System Pipeline: The pipeline uses PyPDF (pdfminer) to extract raw text from the PDF​
MEDIUM.COM
, then splits the text into chunks as described. Chunks (with their source metadata) are stored in Chroma for vector search​
MEDIUM.COM
. At query time, the system generates vector queries (with potential query rephrasing) and retrieves top relevant chunks. These chunks are supplied to an OpenAI GPT-4 model to answer the user’s query. The article provides code snippets for each step (loading PDF, chunking, indexing, querying) and even links to a full Jupyter Colab notebook​
MEDIUM.COM
 for hands-on experimentation. The focus is on balancing quality vs. cost – e.g. using cheaper model variants for intermediate steps (query generation) and reserving more powerful models for final answer synthesis​
MEDIUM.COM
.
URL: Medium – RAG Pipeline for PDF Search
Multimodal RAG for PDFs with Text, Images, and Charts
Author/Org: Pathway.com Engineering Team
Date: June 20, 2024
Summary: This article (an app template from Pathway) demonstrates a production-ready multimodal RAG pipeline for PDF documents that contain not only text but also images, tables, and charts​
PATHWAY.COM
​
PATHWAY.COM
. It showcases how integrating a variety of data types into RAG can significantly enhance the system’s capability to answer complex questions (e.g. in financial documents) by extracting and indexing visual information alongside text. The solution leverages Pathway’s streaming data platform and OpenAI’s multimodal GPT-4.0 (“GPT-4o”).
PDF Chunking & Retrieval: The pipeline performs hierarchical PDF parsing. Each PDF page is parsed to extract textual content as well as detect tables or charts (which are treated as images). For text, conventional chunking is applied with structure-awareness: content is segmented while preserving headings and sections using Pathway’s DoclingParser (maintaining a logical document tree). For tables, a unique approach is used: tables are extracted as images, then GPT-4o is prompted to “explain” each table – converting the table’s image into a detailed textual description​
PATHWAY.COM
. This description is stored as part of the chunk metadata in the vector index, so the system can retrieve table information via text search. All extracted chunks (text passages and GPT-generated table descriptions) are embedded (OpenAI embeddings via GPT-4o) and stored in Pathway’s in-memory vector store​
PATHWAY.COM
. Retrieval is a hybrid of vector similarity and metadata filtering – e.g. one can filter by section headers or by chunk type (text vs table) before vector search, to ensure relevant context is fetched.
System Pipeline: The architecture consists of three key components​
PATHWAY.COM
: (1) Data parsers (Pathway’s DoclingParser and custom logic) ingest PDFs and produce structured chunks; (2) a vector database (Pathway’s built-in vector index) that indexes all chunk embeddings along with metadata (like section hierarchy, page number); and (3) the LLM (OpenAI GPT-4o) which is used at two stages – first during ingestion to interpret images/tables, and later during query time to generate the final answer​
PATHWAY.COM
. When a user query arrives, relevant text chunks and any related table descriptions are retrieved (using vector similarity possibly constrained to relevant document sections). These are passed to GPT-4o which then produces a combined answer using both textual and visual data. The system is designed for real-time sync: Pathway keeps the index updated if PDFs change, and ensures low-latency retrieval. The article includes architecture diagrams and code snippets (Python with Pathway’s API) to illustrate how to set up the pipeline and integrate with OpenAI. This design balances quality (rich multimodal context) with latency by doing heavy parsing upfront and keeping retrieval lightweight at query time.
URL: Pathway Developer Blog – Multimodal RAG for PDFs
Visual RAG over PDFs with Vespa (Demo Application in Python)
Author/Org: Leandro Alves – Vespa Engineering Blog (Yahoo/Oath)
Date: November 19, 2024
Summary: This blog post details the design of a visual Retrieval-Augmented Generation system for PDFs using Vespa (a scalable vector search engine) combined with a vision-language model​
BLOG.VESPA.AI
​
BLOG.VESPA.AI
. The use case here was an enterprise scenario: searching a large collection of PDFs (such as reports) that contain text, scanned pages, and complex figures. The solution employs ColPali, a multimodal embedding technique, to index both text and image content of PDF pages in Vespa, enabling a “What-You-See-Is-What-You-Search” capability. The post covers the system’s architecture, trade-offs made to optimize latency and accuracy, and integration of a generative model for answer formulation.
PDF Chunking & Retrieval: Each PDF is split by pages (each page treated as a document in the index). Using the ColPali approach, every page yields multiple embeddings: textual content is encoded (e.g. with a text encoder), and images/regions are encoded via a vision model into patch embeddings​
BLOG.VESPA.AI
. Vespa indexes these embeddings and allows late fusion search – meaning a query can find relevant pages either via textual similarity or visual similarity. The retrieval step in Vespa is configured with custom ranking profiles that blend modalities. For example, one rank profile (mode) might purely use ColPali’s joint text-image embeddings for similarity, another might also incorporate keyword (BM25) matching​
BLOG.VESPA.AI
. The blog notes that multiple rank profiles were defined to handle different query types, each balancing latency, cost, and quality differently​
BLOG.VESPA.AI
. This means the system can adjust search strategy (vector recall vs. precision, number of candidates, etc.) depending on context – a clear example of engineering for trade-offs between speed and accuracy. After Vespa retrieves the top relevant page(s), the pipeline uses a vision-language generative model (Google’s Gemini 1.5-Flash 8b in the demo) to read the retrieved page content (text + images) and generate the final answer​
BLOG.VESPA.AI
.
System Pipeline: 

High-level architecture of the Visual RAG system using Vespa and a vision-language model. The Vespa engine (top) indexes PDF page content and handles hybrid retrieval, while a separate VLM (Gemini) generates answers using the retrieved page content (text+images)​
BLOG.VESPA.AI
​
BLOG.VESPA.AI
. The pipeline consists of a frontend UI (for query input and result display) connected to a backend service (built with FastAPI/Starlite and Vespa’s Pyvespa). On query, the backend obtains a query embedding (using the same ColPali model) and performs a Vespa query with nearest-neighbor search over embeddings (and optional keyword match)​
BLOG.VESPA.AI
. Vespa returns the top matching page and even highlights which parts (text or image regions) matched best (thanks to ColPali’s patch-level similarity). The relevant page (or snippet of it) is then fed, along with the user’s question, into the Gemini VLM which produces a descriptive answer. The blog provides code and config snippets (Vespa schema, ranking profile setup, etc.) to show how PDF pages are defined as documents, how OCR is applied to scanned PDFs (if needed), and how the HuggingFace Transformers were used for embeddings. By moving heavy computation (vector search, reranking) into Vespa and using a smaller VLM for generation, the system achieves an efficient balance: Vespa handles retrieval at scale (ensuring relevant context is found even among thousands of PDFs), while the VLM focuses on generation with only the necessary page context, keeping latency and costs manageable.
URL: Vespa Blog – Visual RAG over PDFs
Enhancing RAG Performance with Smart Chunking Strategies
Author/Org: Shabna M.T. (IBM Developer Article)
Date: February 2, 2025
Summary: This IBM Developer article offers a deep dive into document chunking techniques and their impact on retrieval-augmented generation performance. Aimed at practitioners, it reviews various chunking strategies (fixed-size vs. dynamic, content-aware chunking, etc.) and provides practical tips on how to choose and tune a chunking approach for a RAG pipeline. The focus is on maximizing retrieval accuracy from knowledge bases like PDFs by preserving semantics and avoiding pitfalls of naive splitting.
PDF Chunking & Retrieval: A key takeaway is the importance of consistently sized and semantically coherent chunks. The author notes that uneven chunk sizes can introduce biases in retrieval – for instance, many very small chunks might disproportionately get high similarity scores, even if they carry less information​
DEVELOPER.IBM.COM
. To avoid such issues, the article suggests “well-balanced chunking”: ensuring chunks are neither too large (which can dilute relevance and hit context window limits) nor too small (which can lose context and game the retriever)​
DEVELOPER.IBM.COM
. It also emphasizes leveraging document structure when chunking PDFs – e.g., splitting by section or heading boundaries, so that each chunk is a logical unit of content. Another strategy covered is metadata tagging: enhancing chunks with metadata like section titles, page numbers, or heading hierarchy, then using these as filters during retrieval. (For example, a query might be restricted to chunks from a specific chapter or with a certain tag.) This hybrid retrieval (vector search + metadata filtering) improves precision by narrowing the search space to relevant portions of the PDF. The article likely demonstrates comparisons of strategies (e.g. paragraph-level vs. heading-level chunking) on retrieval metrics, showing that smarter chunking yields better answer accuracy.
System Pipeline: While the article is more focused on the data preprocessing stage, it situates chunking within the full RAG pipeline. The typical pipeline stages – ingestion, chunking, embedding, indexing, retrieval, and generation – are reviewed with an eye on how chunking strategy affects each. There is discussion of using tools like IBM’s Data Prep Toolkit (DPK) to parse PDFs and apply chunking rules. For instance, one might use DPK or Unstructured to convert a PDF into structured text (maintaining headings, lists, tables as identifiable elements), then apply a custom splitter that treats each top-level section as a chunk or that merges small sub-sections together. By preserving structure and enhancing chunks with context (like “this text was under heading X”), the downstream vector database can return results that are not only similar in content but also contextually relevant. The article includes an architecture diagram illustrating where chunking fits in the pipeline and how it feeds into the vector index and LLM. Overall, this resource serves as a practical guide to optimizing the RAG retrieval stage through better chunk preprocessing, ultimately balancing quality (more relevant context) with performance (not overloading the vector store or LLM with too many or too large chunks).
URL: IBM Developer – Smart Chunking Strategies in RAG 
DEVELOPER.IBM.COM
Mastering RAG: Precision Techniques for Table-Heavy Documents
Author/Org: Ryan Siegler – KX (Tech Blog)
Date: February 24, 2025
Summary: In this engineering blog post, Ryan Siegler explores techniques to improve RAG pipelines when dealing with documents that contain numerous tables (like financial reports or spreadsheets)​
KX.COM
. Tables pose a challenge for RAG because plain text embeddings often fail to capture the structured data they contain, and LLMs can misinterpret numerical values out of context. The article proposes a pipeline that extracts and enriches tables from PDFs, making them more retrievable and interpretable by LLMs. The example use case is querying Meta’s earnings report (a PDF with multiple financial tables)​
KX.COM
.
PDF Chunking & Retrieval: The approach centers on treating each important table as a first-class chunk, rather than letting tables get lost in a sea of text. The author outlines four key steps​
KX.COM
: (1) Precise extraction: use a PDF parser (Unstructured.io in this case) to locate all tables in the document and extract them in a usable format (e.g. CSV or DataFrame)​
KX.COM
. (2) Contextual enrichment: for each table, use an LLM to generate a natural-language description that summarizes the table’s content and context (for example, “This table shows quarterly revenue and profit for 2023…”)​
KX.COM
. The LLM is prompted with the table data plus surrounding text to ensure the description captures the table’s meaning. (3) Format standardization: convert each table into a consistent text format (in this case, Markdown)​
KX.COM
. By representing the table as Markdown, including headers and cells, the structure is preserved in a way an embedding model can ingest (and the LLM can later understand). (4) Unified embedding: combine the LLM-generated description with the Markdown table text to form a single “table chunk”​
KX.COM
, and embed this chunk with a vector embedding model. These enriched table chunks are stored in the vector index alongside regular text chunks from the PDF. This way, the retriever can match user queries to tables either via the table’s content (numbers or keywords in the Markdown) or via the semantic description. The retrieval uses a hybrid strategy: the vector search finds relevant chunks (whether narrative text or tables), and the final answer generation step can incorporate both. By doing this, the pipeline vastly improves the chances that a query about a specific figure (“What was Meta’s Q4 2024 revenue?”) will retrieve the exact table containing that answer, rather than a less precise reference.
System Pipeline: The pipeline begins with using Unstructured.io to parse the PDF into its constituent elements: paragraphs, tables, titles, etc.​
KX.COM
. Text elements are chunked normally (with a sensible token limit), while table elements go through the special handling described above. All chunks get embeddings (the blog uses KDB.AI as the vector database, hinting at very fast vector operations). At query time, a standard RAG retrieval occurs: the user query is vectorized and the top-k relevant chunks are retrieved. Because of the prior steps, those top chunks are more likely to include helpful table data (with descriptive context). The generation step is handled by an LLM (e.g., GPT-4 or Cohere) which receives not just raw table text but the augmented descriptions, enabling it to accurately pull the needed facts. The blog illustrates this with a Colab notebook and diagrams, showing how the answer to a question can be formed by quoting a specific table entry and its context. This design is an example of structured-aware retrieval, where domain-specific data (tables) is handled with extra care to boost overall quality. While it introduces additional preprocessing (LLM calls to describe tables, etc.), the payoff is higher answer accuracy for data-heavy documents – a worthy trade-off in many production scenarios where correctness is paramount.
URL: KX Blog – Table-Heavy Document RAG​
KX.COM
​
KX.COM
LumberChunker: Long-Form Narrative Document Segmentation (RAG Pipeline)
Author/Org: André Duarte, João Marques, et al. (Research, arXiv 2024)
Date: June 25, 2024 (arXiv preprint)
Summary: LumberChunker is an academic but highly applicable contribution that introduces a novel chunking algorithm for very long documents, aimed at improving RAG retrieval and generation quality​
ARXIV.ORG
. Unlike fixed-size or naive semantic chunking, LumberChunker leverages an LLM to dynamically determine optimal chunk boundaries in a text, especially for narrative or book-like documents. The paper presents a benchmark (GutenQA) with 100 long books and demonstrates that LumberChunker’s intelligent segmentation leads to significantly better retrieval of specific facts, nearly matching the effectiveness of manual expert chunking​
ARXIV.ORG
.
PDF Chunking & Retrieval: Although the evaluation is on books, the method is applicable to PDFs (many PDFs like reports or manuals have long narrative sections). The LumberChunker algorithm works in an iterative fashion​
ARXIV.ORG
​
ARXIV.ORG
: it reads through the text and uses an LLM (Gemini 1.0-Pro in experiments) to decide where one chunk should end and the next begin. Essentially, it asks the LLM to identify points where the content “diverges significantly” from the preceding context​
ARXIV.ORG
 – these points likely correspond to topic shifts or new sections. By doing this, it aims to make each chunk semantically self-contained and independent (as independent as possible)​
ARXIV.ORG
. The hypothesis, borne out by results, is that when chunks don’t rely on each other for missing context, a vector retriever can fetch the one relevant chunk more reliably without needing overlapping text. In other words, it avoids the “lost in the middle” issue where important info is split across chunks. For retrieval, standard vector search is used (the paper integrates LumberChunker chunks into a RAG pipeline for QA). Because the chunks are optimized to encapsulate answers, the RAG pipeline can retrieve answers with higher accuracy – the paper reports improved recall@k and DCG@k compared to baseline chunking methods like fixed-length, recursive (hierarchical), or semantic (e.g., sentence-level) splitting​
ARXIV.ORG
. Notably, LumberChunker even outperformed a scenario where a very large context model (with 1.5M token input window) tried to answer questions without retrieval – underscoring that smart chunk-and-retrieve can beat brute-force large context usage​
ARXIV.ORG
.
System Pipeline: The research outlines how to plug LumberChunker into a typical RAG pipeline. During ingestion, instead of using a simple text splitter, you use the LLM-in-the-loop to segment the document. This does add computational cost at indexing time (essentially performing a linear pass with an LLM prompt at each step), but indexing is done offline. Once chunks are created, they are embedded and indexed in a vector store as usual. The retriever is unchanged (still does k-NN search on embeddings), but now the chunks are higher quality units. The generation step also remains the same, except that because LumberChunker chunks are more comprehensive, the LLM has all necessary context in the retrieved chunk and thus produces more accurate answers. The paper includes diagrams and an open-source implementation​
ARXIV.ORG
 (with a GitHub link) to encourage practitioners to experiment. From an engineering perspective, LumberChunker offers a trade-off: slightly heavier preprocessing in exchange for better runtime performance (fewer chunks to search) and better answer quality. It’s practical for pipelines where documents are static or infrequently updated (e.g., books, archived PDFs) and where maximizing accuracy is worth the upfront cost.
URL: arXiv – LumberChunker Paper​
ARXIV.ORG
​
ARXIV.ORG
RAG with a PDF using LlamaIndex and Vertex AI (Google Cloud)
Author/Org: Mete Atamel (Google Cloud Developer Advocate)
Date: March 24, 2025
Summary: In this Google Cloud Community blog post, Mete Atamel demonstrates how to build a simple RAG pipeline on GCP using a PDF as the knowledge source​
MEDIUM.COM
. It uses LlamaIndex (formerly GPT Index) as the orchestration framework, Google’s Vertex AI for embeddings and LLMs (specifically the Embedding API and the Gemini model for generation), and shows integration with GCP services. The example highlights a lightweight pipeline suitable for Q&A on a single PDF (here, a Cymbal Starlight product brochure).
PDF Chunking & Retrieval: The approach is relatively straightforward: the PDF is read and each page is treated as a document node​
MEDIUM.COM
 using LlamaIndex’s SimpleDirectoryReader (which under the hood uses PyMuPDF or similar to extract text). LlamaIndex then applies a SentenceSplitter to break down each page’s text into chunks of up to 1024 tokens with a small overlap​
MEDIUM.COM
. The choice of sentence-based splitting ensures chunks align with natural language boundaries. The chunks are fed to Vertex AI’s embedding model (text-embedding-005), generating embeddings that are stored in an in-memory SimpleVectorStore (managed by LlamaIndex)​
MEDIUM.COM
. The retrieval step uses these embeddings: at query time, the query is embedded with the same model, and LlamaIndex retrieves the top-k similar chunks. There’s no complex hybrid filtering in this simple example, but LlamaIndex does allow adding metadata (e.g., page numbers or section titles) if needed. The focus here was on demonstrating basic RAG functionality with minimal code.
System Pipeline: The pipeline can be summarized in a few steps​
MEDIUM.COM
: Read PDF -> Split into chunks -> Embed chunks -> Store index -> Query -> Generate answer. The blog shows code for each part. After embedding and indexing, a QueryEngine is created by pairing the index with a Vertex AI text generation model (Google’s Gemini 2.0 model in “flash” mode for speed)​
MEDIUM.COM
. When a user question is asked, the QueryEngine retrieves relevant chunk(s) and then calls the LLM to produce an answer using those chunks as context. The answer is then printed out. The author also demonstrates how to persist the vector index to disk and load it later​
MEDIUM.COM
, which is useful for production scenarios (so you don’t have to re-process the PDF each time). This design is optimized for simplicity and cost-effectiveness: it uses managed services (Vertex AI) to avoid maintaining custom models, and it processes a small number of chunks, which keeps latency low. While it may not have advanced features like caching, re-ranking, or elaborate chunking, it’s a practical starting point for developers. The pipeline’s modular nature (LlamaIndex abstraction) means one can later swap in more advanced chunkers or a more powerful vector store (like Firestore or Pinecone) – in fact, the author references examples with Annoy and Firestore indices as alternatives​
MEDIUM.COM
.
URL: Google Cloud Blog (Medium) – PDF RAG with LlamaIndex​
MEDIUM.COM
​
MEDIUM.COM
Each of these resources provides valuable insights into building RAG systems with PDF knowledge bases. From company engineering blogs to research papers, the common threads are: preserving document structure and semantics during chunking, combining vector search with metadata or reranking for precision, and thoughtful architecture choices to meet latency and cost constraints. By studying these designs, practitioners can mix and match techniques (e.g. using LLM-based chunkers like LumberChunker, or table enrichment from KX’s approach) to build robust PDF question-answering systems in their own organizations.






Citations
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
instructionals with varying success, you’re not alone. You might have set up a basic RAG pipeline, like the LlamaIndex example that runs in just five lines of code, only to find the results didn’t cut it for production use cases. Slow processing times, high costs, unpredictable outcomes with complex documents, and difficulty debugging are all well-known challenges. And even once you’ve got a better handle on the application, you may struggle quantifying the performance of your pipeline and been reduced to manually QAing the results.
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
Link to Jupyter Notebook: RAG Pipeline Example
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
Chunking is crucial for building effective Retrieval-Augmented Generation (RAG) pipelines, especially with long documents like PDFs, because it breaks text into
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
match at L235 index = Chroma.from_documents(documents=chunks, embedding=OpenAIEmbeddings())
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
Different libraries can be used to extract text from PDFs. If you’d like to learn more about the tool landscape for extracting from PDFs, check out my article on Comparing PDF parsers.
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
Add chunks to vector database
Faviconmedium.com
Building an Accurate, Tested RAG Pipeline for PDF Document Search with LangChain | by Brian McGough | Medium
* Previously used GPT 3.5 turbo, but OpenAI recently released GPT-4o-mini, which replaces 3.5 turbo. It’s preferred to use these cheaper models for development due to speed and cost-effectiveness. The application developed here will make at least seven API calls per query, and that can add up quickly, especially when you add more test cases. Also, consider using cheaper models to be developing for the worst case — if you achieve good results here, upgrading to GPT-4o ensures even better performance. You can also segment your workflow to use different models for various tasks if needed, for example, use GPT-4o-mini for generating queries GPT-4o for the final query once the context has been extracted.
Faviconpathway.com
Multimodal RAG for PDFs with Text, Images, and Charts | Pathway
Multimodal Retrieval-Augmented Generation (MM-RAG) systems are transforming the way you enhance Language Models and Generative AI. By incorporating a variety of data types within one application, these systems significantly expand their capabilities and applications.
Faviconpathway.com
Multimodal RAG for PDFs with Text, Images, and Charts | Pathway
Multimodal Retrieval Augmented Generation (RAG) enhances LLM applications by incorporating text, images, audio, and video into the generation process. These systems retrieve relevant data from external sources and integrate it into the model’s prompt, enabling more accurate and contextually informed responses. This is particularly useful for understanding and generating content from diverse data formats. For example, in financial contexts, Multimodal RAG can efficiently interpret PDFs with complex tables, charts, and visualizations, significantly improving response accuracy.
Faviconpathway.com
Multimodal RAG for PDFs with Text, Images, and Charts | Pathway
1. Parsing Process: Tables are extracted as images, and GPT-4o then explains the content of these tables in detail. The explained content is saved with the document chunk into the index for easy searchability. 2. Answering Questions: Questions are sent to the LLM with the relevant context, including parsed tables. This allows the generation of accurate responses based on the comprehensive multimodal context.
Faviconpathway.com
Multimodal RAG for PDFs with Text, Images, and Charts | Pathway
* BaseRAGQuestionAnswerer Class: Integrates foundational RAG components. * GPT-4o by Open AI: Used for extracting and understanding multimodal data, generating vector embeddings, and for answering queries with retrieved context. * Pathway: Provides real-time synchronization, secure document handling, and a robust in-memory vector store for indexing.
Faviconpathway.com
Multimodal RAG for PDFs with Text, Images, and Charts | Pathway
* BaseRAGQuestionAnswerer Class: Integrates foundational RAG components. * GPT-4o by Open AI: Used for extracting and understanding multimodal data, generating vector embeddings, and for answering queries with retrieved context. * Pathway: Provides real-time synchronization, secure document handling, and a robust in-memory vector store for indexing.
Faviconpathway.com
Multimodal RAG for PDFs with Text, Images, and Charts | Pathway
Here we use Open AI’s popular Multimodal LLM, GPT-4o. It’s used at two key stages:
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
In this blog post, we will do a deep dive into the process of building a live demo application showcasing Visual RAG over PDFs using ColPali embeddings in Vespa. We will describe the architecture, user experience, and the tech stack used to build the application.
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
Thomas joined Vespa as a Senior Software Engineer in April 2024. His last assignment in his previous role as an AI consultant was actually to build a RAG application over a large collection of PDFs using Vespa.
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
> Note that the term ColPali is overloaded to mean two things: > > 1. A particular model with a corresponding paper1 that trains a LoRa-adapter on top of a VLM (PaliGemma) to generate joint embeddings for text and images (one embedding per patch in the image) to be used for “late interaction”, building upon the ColBERT approach to vision language models. > 2. It also represents a direction in visual document retrieval, combining the power of VLMs with efficient late interaction mechanisms. This direction is
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
# 1. Pure Colpali
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
One of the most underrated features of Vespa is the phased ranking feature. It allows you to define multiple rank profiles, each with different (or inherited) ranking phases, that can be executed on the content nodes (first and second phase) or the container node(s) (global phase).
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
OpenAI, Anthropic, and Google have all released great Vision Language Models (VLMs) in the past year, and the field is moving fast. We wanted a smaller model for performance reasons, and with the recently improved Developer experience of Google’s Gemini API, we decided to go with `gemini-1.5-flash-8b` for this demo.
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
With our tech stack in place, we could now start building the application. The high-level architecture of the application is as follows:
Faviconblog.vespa.ai
Visual RAG over PDFs with Vespa - A demo application in Python | Vespa Blog
In our application,the yql used for this ranking mode is:
developer.ibm.com
Enhancing RAG performance with smart chunking strategies
However, uneven chunk sizes can lead to biases, where smaller chunks may dominate retrieval, even if they are less semantically relevant.
Faviconkx.com
Mastering RAG: Precision techniques for table-heavy documents | KX
The retrieval-augmented generation (RAG) revolution has been moving forward for some time. Still, it’s not without issues, especially when handling non-text elements like images and tables. One challenge is the accuracy reduction whenever RAG retrieves specific values from tables. It’s even worse when the documents have multiple tables on related topics, such as an earnings report.
Faviconkx.com
Mastering RAG: Precision techniques for table-heavy documents | KX
Objective: Build a RAG pipeline for Meta’s earnings report data to retrieve and answer questions from the document’s text and multiple tables.
Faviconkx.com
Mastering RAG: Precision techniques for table-heavy documents | KX
1. Precise extraction: Cleanly extract all tables from the document. 2. Contextual enrichment: Leverage an LLM to generate a robust, contextual description of each table by analyzing the extracted table and surrounding document content. 3. Format standardization: Employ an LLM to convert tables into a uniform markdown format, enhancing embedding efficiency and LLM comprehension. 4. Unified embedding: Create a ‘table chunk’ by combining the contextual description with the markdown-formatted table, optimizing it for vector database storage and retrieval.
Faviconkx.com
Mastering RAG: Precision techniques for table-heavy documents | KX
Step 1: Precise extraction
Faviconkx.com
Mastering RAG: Precision techniques for table-heavy documents | KX
description of each table by analyzing the extracted table and surrounding document content. 3. Format standardization: Employ an LLM to convert tables into a uniform markdown format, enhancing embedding efficiency and LLM comprehension. 4. Unified embedding: Create a ‘table chunk’ by combining the contextual description with the markdown-formatted table, optimizing it for vector database storage and retrieval.
Faviconkx.com
Mastering RAG: Precision techniques for table-heavy documents | KX
3. Format standardization: Employ an LLM to convert tables into a uniform markdown format, enhancing embedding efficiency and LLM comprehension. 4. Unified embedding: Create a ‘table chunk’ by combining the contextual description with the markdown-formatted table, optimizing it for vector database storage and retrieval.
Faviconarxiv.org
match at L70 In this paper, we propose LumberChunker, a novel text segmentation method based on the principle that retrieval efficiency improves when content chunks are as independent as possible from one another. This independence is best achieved by
Faviconarxiv.org
the paper’s main scope, further details are provided in Appendix E. We compare our approach with other RAG pipeline variants using different chunking techniques, including manually created chunks, which we consider the gold standard for optimal retrieval. We also employ non-RAG baselines like Gemini 1.5 Pro (Reid et al., 2024), capable of processing up to 1.5 million input tokens, and a closed-book setup
Faviconarxiv.org
propose LumberChunker, a method leveraging an LLM to dynamically segment documents, which iteratively prompts the LLM to identify the point within a group of sequential passages
Faviconarxiv.org
3.1 LumberChunker Our main proposed contribution is a novel method for document segmentation named LumberChunker, which employs an LLM to dynamically segment documents into semantically independent
Faviconarxiv.org
is given as input to the LLM (we choose Gemini 1.0-Pro (Team et al., 2023)), which we instruct to pinpoint the specific paragraph within Gi where the content is perceived to diverge significantly from the preceding context. This detection marks the end of a chunk. The document keeps being sequentially partitioned into chunks in a cyclical manner, with the starting point of each new Gi+1 group being the paragraph identified in the previous iteration.
Faviconarxiv.org
In this paper, we propose LumberChunker, a novel text segmentation method based on the principle that retrieval efficiency improves when content chunks are as independent as possible from one another. This independence is best achieved by
Faviconarxiv.org
joaodsmarques/LumberChunker quences, like the recent incident where a lawyer cited fictitious cases produced by ChatGPT (OpenAI, 2022) in court, resulting in sanctions for the
Faviconmedium.com
RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI | by Mete Atamel | Google Cloud - Community | Mar, 2025 | Medium
Previously, I showed how to do RAG with a PDF using LangChain and Annoy Vector Store and RAG with a PDF using LangChain and Firestore Vector Store. Both used a PDF as the RAG backend and used LangChain as the LLM framework to orchestrate RAG ingestion and retrieval.
Faviconmedium.com
RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI | by Mete Atamel | Google Cloud - Community | Mar, 2025 | Medium
Before you can use a PDF in a RAG pipeline, you need to first load the PDF into documents with `SimpleDirectoryReader`. Each page in the PDF becomes a separate document:
Faviconmedium.com
RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI | by Mete Atamel | Google Cloud - Community | Mar, 2025 | Medium
text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
Faviconmedium.com
RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI | by Mete Atamel | Google Cloud - Community | Mar, 2025 | Medium
Finally, use `VectorStoreIndex.from_documents` to split the documents into smaller chunks and turn them into embeddings:
Faviconmedium.com
RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI | by Mete Atamel | Google Cloud - Community | Mar, 2025 | Medium
Read PDF into documents Initialize embedding model Index documents Initialize the query engine with the model Question: What is the cargo capacity of Cymbal Starlight? Response: The cargo capacity of the Cymbal Starlight 2024 is 13.5 cubic feet.
Faviconmedium.com
RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI | by Mete Atamel | Google Cloud - Community | Mar, 2025 | Medium
print("Initialize the query engine with the model") llm = Vertex(model="gemini-2.0-flash-001") query_engine = index.as_query_engine(llm=llm)
Faviconmedium.com
RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI | by Mete Atamel | Google Cloud - Community | Mar, 2025 | Medium
Storage