## Multilingual RAG
#### Technical Assessment - 10MS

#### Shadab Hafiz Choudhury

### Setup

On a Python 3.11 environment.

1. Install required packages.

```bash
pip install -r requirements.txt
```

2. Create a top-level folder called `envs`. Inside it, create a `keys.yaml` file. This file should be formatted like this:
```yaml
openai:
    api_key: sk-proj-restofthekey
```

3. Enter an OpenAI API key into the aforementioned file. I assume you have a key somewhere around. Obviously, I can't share my personal keys here.

    But if you don't have any keys at all, please let me know.


4. If running on a new set of documents, first delete the contents of `knowledge_base/database`. Then place the documents in the `knowledge_base/data` folder.
   
    Then run vectorize_data.py in order to store the documents in the vector database.

### To Run

1. Launch API Server

```bash
cd application
uvicorn main:app --host 127.0.0.1 --port 8005
```

2. Launch Gradio Interface

```bash
python run gradio_app.py
```

3. Open `127.0.0.1:3005`, or, if you changed any of the ports, whichever port gradio is outputting to.

4. Enter the question and click on submit.

### Project Structure

```text
Multilingual_RAG
│
├─── application\
│    ├─── main.py - This file contains the FastAPI REST API endpoints. Start this to run the API locally.
│    ├─── gradio_app.py - Run this file to start up the GUI. This must be run after the API endpoints are running.
│    └─── retrieval.py - Contains the code to carry out retrieval from the vector database.
│
├─── knowledge_base\
│    │
│    ├─── data\
│    │    └─── HSC26-Bangla1st-Paper.pdf - Data files that are used for text extraction and storage.
│    │
│    ├─── database\ - Contains local storage files for the Qdrant vector database.
│    │
│    ├─── output\ - Contains text extracted from PDF for temporary storage, for testing or debugging.
│    │
│    └─── preprocessing\
│         ├─── preprocess_data.py - This file contains functions for preprocessing the data
│         └─── HSC26-Bangla1st-Paper.pdf - This file contain functions for loading the data, embedding it, then uploading to vector DB.
│ 
└─── envs\
     └─── keys.yaml - Contains environment variables and API keys.
```

### Sample Responses

**Q: Why was uncle's mood so heavy?**

_A: ১৮। চাকরি চলে গেল।_

**Q: What do they say about an unpredictable character?**

_A: অব্মূলযা কনি_

**Q: োোলক ভাগ্য দেিতাি প্রধান এলজন্ট ি াি কািণ, তাি-**

_A: দোলক ভাগ্য বা "ফলিত জ্যোতিষ" প্রধানত নিচের কিছু কারণে গুরুত্বপূর্ণ: (contd)_

**Q: রবীন্দ্রনাথ ঠাকুর এর জন্ম কবে?**

_A: রবীন্দ্রনাথ ঠাকুরের জন্ম ৭ মে ১৮৬১ সালে।_


### Tech Stack

| Task               | Library      |
|--------------------|--------------|
| PDF Parsing        | PDFMiner.six |
| Text Cleaning      | BNLP Toolkit |
| Vector Database    | Qdrant       |
| REST API           | FastAPI      |
| Front-End          | Gradio       |
| Text Embedding     | HuggingFace  |
| Response Generation | OpenAI       |

### API Documentation

1. **GET/**

    Summary: Read Root

    URL: /

    Responses: 200 OK – Successful Response


2. **POST/rag_chat**

    Summary: Takes a text input and processes it (e.g., RAG chat or GPT processing).

    URL: /rag_chat

    Request Body (application/json): {  "text": "Your input text here"   }

    Responses: 200 OK – Successful Response, 422 Unprocessable Entity – Validation Error (e.g., missing text field).

### Q/A

1. PDFminer was used to parse the PDF file. The biggest challenge was simply organizing and grouping the responses in a sensible way.
I.e. we want to keep an MCQ Question and its answers together, but separate lines for paragraph chunking or section breaks or between different questions.
I elected to not bother solving this problem, but if I needed to I would've tried parsing results based on the structure (i.e. if there's a group of 4 lines formatted like A) Word \n B) Word), I would've grouped them.
That is **a lot** of work and I'm not doing all that for free.


2. I used paragraph based chunking, separating on newlines between paragraphs. However, the bigger focus was on keeping single individual lines correctly together. 

    For instance, for an MCQ question, we want the whole question to be intact for retrieval purposes, and for stories we want large enough sections to give context to retrieval content.


3. I used the `intfloat/multilingual-e5-base` model, which is a text embedding model based on the multilingual Roberta. It's been fine-tuned on 16 languages including Bengali, and has very strong performance on MTEB despite being a small (280M params) model.

    I would've also considered trying out two separate models for English and Bengali, but I didn't have a good knowledge of which Bengali embedding model's good.


4. I'm using cosine similarity. It's the de facto, standard approach. It doesn't actually seem to work well and I would've preferred different approaches such as:
   1. Named Entity Recognition across the database. This is a better approach than cosine similarity for **questions** rather than general text searching.
   2. System 2 prompting to validate the results of the retrieval. LLMs are quite good at re-ranking information, so instead of a similarity-score based ranking I'd let an LLM sort through the retrieved text for the most relevant info.


5. I do not ensure the comparison is meaningful, and if I did I would've used the approaches I described in the previous point. For queries that are vague and missing context, similarity search does help, but the number of items to retrieve would need to be set high and a lot of reranking done after the fact.


6. Not really. Biggest issue with my implementation is the chunking. The embedding model makes a small difference (embedding methods for retrieval have only improved by a tiny margin over time, from a research perspective, for a long time), but a better retrieval approach would work wonders. Finally, a bigger document would make no difference as this is retrieval, not training or fine-tuning.

