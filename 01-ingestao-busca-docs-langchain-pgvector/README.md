# Desafio MBA Engenharia de Software com IA - Full Cycle

## STEPS TO CONFIGURE THE PROJECT

### 1. Create a virtual environment

Run the following command to initialize a new virtual environment:

````bash
python -m venv venv
````

A new folder named `venv` will be created in the root folder. Now, run the following command to activate the virtual environment:

| ON UNIX | ON WINDOWS |
| :----:  | :--------: |
| `source venv/bin/activate` | `venv\Scripts\activate` |

### 2. Install the needed dependencies

Run the following command to install the dependencies:

````bash
pip install -r requirements.txt
````

### 3. Configure environment variables

Create a `.env` file in the root directory with the following variables:

````text
# Can be "openai" or "goggle"
EMBEDDING_PROVIDER=the_provider

# OpenAI Configuration (required if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_AGENT_MODEL=gpt-4o-mini

# Google Configuration (required if using Google)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_EMBEDDING_MODEL=models/text-embedding-004
GOOGLE_AGENT_MODEL=gemini-1.5-flash

# PostgreSQL Vector Database
PGVECTOR_URL=postgresql://user:password@localhost:5432/vectordb
PGVECTOR_COLLECTION=documents

# Application Paths
PDF_PATH=document.pdf
````

#### Embedding and Chat Model Provider Options

The application supports multiple embedding and chat model providers:

- **OpenAI** (`EMBEDDING_PROVIDER=openai`): Uses OpenAI's embedding models like `text-embedding-3-small` and chat model like `gpt-5-nano`
- **Google** (`EMBEDDING_PROVIDER=google`): Uses Google's Generative AI embedding models like `gemini-embedding-001` and chat model like `gemini-flash-2.5-flash-lite`

Simply set the `EMBEDDING_PROVIDER` variable to your preferred provider and ensure the corresponding API key and model are configured.

### 4. Update the `requirements.txt` file

If you want to use a new dependency, you need to install and register it with this command:

````bash
pip install "thedepencyname" && pip freeze > requirements.txt
````

## STEPS TO EXECUTE THE PROJECT

Activate the virtual environment generated previously:

````basH
source venv/bin/activate
````

So, you need to check if you have the vector database running. If you are using the provided `docker-compose.yml` file, run the following command to start the database container:

````bash
docker-compose up -d
````

Now you need to ingest the document file into the vector database executing the related Python file:

````bash
python run_ingest.py
````

Finally, execute the the Python chat file to start the flow:

````bash
python run_chat.py
`````
---
