# Welcome To Our Hackathon

### Your Mission 

We have been growing DevMornings for almost two years now and with your help the past two months have been the best yet.  So let's keep the group growing and build some cool s*** together!

This repo was created so all of us can work together to create DevMorning's first website together using AI.  Both to build and to allow for some cool features on the web.  Our mentors will be here every step of the way.

### How Our Hackathon Works

To help our organization grow and give our members access to tech leaders, exclusive technology, and incredible opportunities we want to build a website.  Not one of those boilerplate websites that everyone has but a custom made full-stack application that will grab the attention of its viewers.

Help us!

Since we have no idea what we want to build we can decide together.  Decide what you want to learn and we will work together to code a real life and published project.  One that you'll be able to show off as part of your portfolio.

_Steps to Building a Software Product_

![Hackathon-Template-3](https://github.com/user-attachments/assets/14ce3501-8819-4bf5-ae2f-ce2942d8420f)



## 🚀 Getting Started

1. Clone this repository
2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

## 📦 Project Structure

```
├── public/
│ └── favicon.svg
├── src/
│ ├── components/
│ │ └── Header.astro
│ ├── layouts/
│ │ └── Layout.astro
│ └── pages/
│ └── index.astro
├── astro.config.mjs
├── package.json
├── tailwind.config.cjs
└── tsconfig.json
```

# 🚀 Generative AI App Roadmap (Astro + NestJS + OpenAI + MongoDB Vector Search)

A structured end-to-end guide to building a production-ready Generative AI application using **Astro, NestJS, OpenAI, and MongoDB Vector Search**. This guide covers everything from embedding company documents, storing vectors, retrieving data, and using prompt engineering for intelligent AI responses.

---

## 📌 Phase 1: Define the Problem & System Design

### 🎯 Goal:
- Define the problem statement (e.g., AI-powered document search, chatbot, summarization).
- Choose the AI task (e.g., text generation, question-answering, summarization).
- Define user inputs (e.g., text queries, document uploads).
- Determine output format (e.g., plain text, structured responses).
- Identify the retrieval approach (e.g., MongoDB Vector Search, RAG).

### 🛠 Tech to Learn:
- AI Basics: Generative AI, RAG (Retrieval-Augmented Generation).
- Vector Search: MongoDB Atlas Vector Search.
- **Astro & NestJS**: Full-stack development.

---

## 📌 Phase 2: Data Collection & Storage

### 🎯 Goal:
- Collect company documents (e.g., PDFs, Word, CSVs, JSON).
- Store documents efficiently in MongoDB.
- Generate and store vector embeddings.

### 🔥 Steps:
#### Set Up MongoDB Atlas:
1. Create a database for documents & embeddings.
2. Enable Vector Search.

#### Install Dependencies:
```bash
npm install openai mongoose @nestjs/mongoose
```

#### Store Documents in MongoDB:
```ts
const documentSchema = new mongoose.Schema({
  content: String,
  embedding: { type: Array, default: [] },
});
```

#### Convert Documents to Embeddings:
```ts
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function generateEmbedding(text: string) {
  const response = await openai.embeddings.create({
    input: text,
    model: 'text-embedding-ada-002',
  });

  return response.data[0].embedding;
}
```

#### Store Vectors in MongoDB:
```ts
async function storeDocument(content: string) {
  const embedding = await generateEmbedding(content);
  await DocumentModel.create({ content, embedding });
}
```

### 🛠 Tech to Learn:
- MongoDB Atlas Vector Search.
- OpenAI Embeddings API.
- NestJS with MongoDB.

---

## 📌 Phase 3: Data Preprocessing

### 🎯 Goal:
- Clean and process unstructured data.
- Implement document chunking for better embeddings.
- Store structured metadata for retrieval.

### 🔥 Steps:
#### Remove Unnecessary Sections:
```ts
function cleanText(text: string): string {
  return text.replace(/(Disclaimer|Footer|Further Support).*/g, '');
}
```

#### Chunk Large Documents:
```ts
function chunkText(text: string, chunkSize = 500) {
  return text.match(new RegExp(`.{1,${chunkSize}}`, 'g'));
}
```

### 🛠 Tech to Learn:
- Text Preprocessing (Regex, Chunking, Stopwords Removal).
- LangChain for Text Splitting.

---

## 📌 Phase 4: Model Training & Fine-Tuning (Optional)

### 🎯 Goal:
- Train a custom OpenAI model if needed.
- Fine-tune responses for specific industry terms.

### 🔥 Steps:
#### Prepare Training Data (JSONL Format):
```json
{"messages": [{"role": "system", "content": "You are a financial assistant."}, {"role": "user", "content": "What is an ETF?"}, {"role": "assistant", "content": "An ETF is an exchange-traded fund."}]}
```

#### Upload and Train in OpenAI:
```bash
openai api fine_tunes.create -t dataset.jsonl -m gpt-4
```

### 🛠 Tech to Learn:
- Fine-tuning OpenAI models.
- Prompt Engineering for better responses.

---

## 📌 Phase 5: Retrieval System Implementation

### 🎯 Goal:
- Implement vector search to find relevant data fast.
- Use MongoDB Vector Search to retrieve the best-matching document.

### 🔥 Steps:
#### Perform Vector Search Query:
```ts
async function searchDocuments(query: string) {
  const queryEmbedding = await generateEmbedding(query);

  return await DocumentModel.find({
    $vectorSearch: {
      queryVector: queryEmbedding,
      path: 'embedding',
      numCandidates: 10,
      limit: 5,
    },
  });
}
```

#### Retrieve Data & Send to OpenAI for Response:
```ts
async function generateAIResponse(query: string) {
  const relevantDocs = await searchDocuments(query);

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'Use the following documents to answer the user query:' },
      ...relevantDocs.map(doc => ({ role: 'user', content: doc.content })),
      { role: 'user', content: query },
    ],
  });

  return response.choices[0].message.content;
}
```

### 🛠 Tech to Learn:
- MongoDB Vector Search Queries.
- Retrieval-Augmented Generation (RAG).

---

## 📌 Phase 6: API Development (NestJS)

### 🎯 Goal:
- Build a REST API to handle AI queries.
- Expose endpoints for querying AI-generated responses.

### 🔥 Steps:
#### Create AI Service:
```ts
@Injectable()
export class AIService {
  async processQuery(query: string) {
    return await generateAIResponse(query);
  }
}
```

#### Create Controller:
```ts
@Controller('ai')
export class AIController {
  constructor(private readonly aiService: AIService) {}

  @Post('query')
  async handleQuery(@Body() data: { query: string }) {
    return this.aiService.processQuery(data.query);
  }
}
```

### 🛠 Tech to Learn:
- NestJS Controllers & Services.
- API Development Best Practices.

---

## 📌 Phase 7: Frontend Integration (Astro)

### 🎯 Goal:
- Create an Astro UI to interact with AI.
- Send queries to the backend and display results.

### 🔥 Steps:
#### API Call from Astro:
```ts
async function fetchAIResponse(query: string) {
  const res = await fetch('/api/ai-query', {
    method: 'POST',
    body: JSON.stringify({ query }),
  });
  return res.json();
}
```

#### Create UI Component:
```astro
---
import { createSignal } from 'solid-js';
const [query, setQuery] = createSignal('');
const [response, setResponse] = createSignal('');
async function handleSubmit() {
  const data = await fetchAIResponse(query());
  setResponse(data);
}
---
<input type="text" value={query()} onInput={(e) => setQuery(e.target.value)} />
<button onClick={handleSubmit}>Ask AI</button>
<p>{response()}</p>
```

### 🛠 Tech to Learn:
- Astro Components.
- API Integration.

---

## 📌 Phase 8: Deployment
- Deploy Astro on **Vercel**.
- Deploy NestJS on **AWS/GCP**.
- Use **MongoDB Atlas** for storage.

