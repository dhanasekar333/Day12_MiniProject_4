# 🤖📚 The Game of Thrones Question Robot

Welcome to a tiny robot that reads a book and answers questions about it! 🐉✨

This project is a simple **PDF question-and-answer chatbot**. You give it a PDF, ask a question, and it looks for the answer inside that PDF.

> Think of it like giving a very good book-reader a highlighter, a memory, and a talking voice. 📖🖍️💬

## What Is This About? 🧐

Imagine a huge storybook on a table. You ask:

> “Who is Jon Snow?”

Instead of making you search every page, the robot:

1. Reads the storybook.
2. Cuts it into smaller pieces.
3. Makes a special “meaning map” for every piece.
4. Finds the pieces closest to your question.
5. Asks a local AI helper to answer using only those pieces.

That is what this project does with `Game of thrones.pdf`. 🏰

## The Problem: Before and After 🔍

### Before: finding an answer the hard way 😵

- Open a long PDF.
- Search many pages.
- Read lots of unrelated words.
- Forget what you asked five minutes ago.

### After: ask the robot 🤖

- Type a question.
- The robot finds useful parts of the PDF.
- The robot answers from the document.
- The robot remembers your earlier questions.

| Without the robot | With the robot |
|---|---|
| Search page by page 📄 | Ask in normal words 💬 |
| Read unrelated text 🥱 | See relevant text 🎯 |
| Forget the conversation 🤔 | Continue follow-up questions 🧠 |
| Rebuild everything every time 🐌 | Reuse the saved index ⚡ |

## Project Folder 📁

```text
Day12_MiniProject_4/
├── project.py              # The chatbot's instructions
├── requirements.txt        # The helper packages it needs
├── Game of thrones.pdf     # The book/document it reads
├── faiss_index/
│   └── index.faiss         # The saved meaning map
└── .models/                # Downloaded language-model files
```

## Examples: The Robot's Big Jobs 🎯

### 1. Read a PDF like a helper 📖

**Fun story:** The robot is handed a very big storybook. It cannot hold the whole book in its tiny head at once, so it cuts the book into friendly-sized puzzle pieces.

**What the code does:** `PyPDFLoader` opens the PDF. `RecursiveCharacterTextSplitter` divides the text into chunks with a little overlap, so important sentences are less likely to be cut apart.

**What we learned:** Big information is easier to search when it is divided into small, useful pieces.

### 2. Build a smart map of meaning 🗺️

**Fun story:** Each puzzle piece gets a magic sticker showing what it means. Pieces about dragons get near other dragon pieces, even when they do not use exactly the same words.

**What the code does:** `HuggingFaceEmbeddings` turns each text chunk into numbers. FAISS stores those numbers so similar questions can quickly find similar chunks.

**What we learned:** Computers can compare the meaning of words, not just exact spelling.

### 3. Reuse the map instead of rebuilding it ⚡

**Fun story:** If the robot already made its map yesterday, it keeps the map in a box and opens it today. It does not redraw the whole map.

**What the code does:** The program checks for `faiss_index`. If it exists, it loads it. Otherwise, it creates the index and saves it.

**What we learned:** Saving finished work makes the next start much faster.

### 4. Choose quick chat or deeper search 🔎

**Fun story:** The robot has two pairs of glasses:

- **Chat glasses:** look at 4 useful pieces.
- **Deep glasses:** look at 8 useful pieces for a wider answer.

**What the code does:** `RunnableBranch`-style chain setup is represented by two chains: one uses `k=4`, and the other uses `k=8`. The selected mode chooses the chain.

**What we learned:** One tool can offer a quick answer or a more careful answer.

### 5. Remember separate conversations 🧠

**Fun story:** Alice and Bob each have their own notebook. Alice's questions do not get mixed into Bob's notebook.

**What the code does:** `session_history()` stores messages using a session ID, which comes from the user's name. `RunnableWithMessageHistory` sends earlier messages along with the next question.

**What we learned:** A chatbot feels much more helpful when it remembers the current conversation.

### 6. Print a little report at the end 🧾

**Fun story:** When story time ends, the robot counts how many questions and answers happened.

**What the code does:** `inspect_session()` reports the session ID, message counts, first question, and latest answer.

**What we learned:** Small reports help us understand how a program was used.

## How It Works Technically, In Simple Steps 🛠️

1. 📄 Load `Game of thrones.pdf`.
2. ✂️ Split the document into chunks of text.
3. 🔢 Turn every chunk into a list of numbers called an embedding.
4. 🗃️ Put those number-lists into a FAISS index.
5. 💾 Save the index, or load it if it already exists.
6. 🕵️ Create a normal retriever that finds 4 chunks.
7. 🔬 Create a deep retriever that finds 8 chunks.
8. 🧩 Put the matching chunks into the AI prompt as context.
9. 💬 Ask Ollama's `llama3.2:3b` model to answer.
10. 🧠 Add the question and answer to the correct session memory.
11. 🧾 Show a session summary when the user types `quit`.

The most important safety rule is in the prompt:

> Answer using the context. If the answer is not there, say “I don't know.”

That helps the robot stay close to the document instead of inventing a story. 🚦

## Files Explained 🗂️

| File or folder | What it does | Easy picture |
|---|---|---|
| `project.py` | Runs the whole chatbot | The robot's brain 🤖 |
| `requirements.txt` | Lists Python packages | A shopping list 🛒 |
| `Game of thrones.pdf` | Supplies the information | The storybook 📖 |
| `faiss_index/index.faiss` | Saves searchable document data | A meaning map 🗺️ |
| `.models/` | Stores downloaded embedding files | The robot's toolbox 🧰 |

## Key Concepts Table 💡

| Concept | Simple meaning | Used here for |
|---|---|---|
| PDF loader | Opens a PDF | Reading the storybook |
| Text splitter | Cuts text into pieces | Making searchable chunks |
| Embedding | Numbers that describe meaning | Comparing ideas |
| Vector store | A box for meaning numbers | Keeping the map |
| Retriever | A finder | Choosing useful chunks |
| Prompt | Instructions for the AI | Explaining the robot's job |
| Chat model | The talking helper | Writing the answer |
| Session memory | A conversation notebook | Remembering follow-up questions |
| `k=4` / `k=8` | How many chunks to find | Quick or deep mode |

## Reusable Pattern: Ask Questions About Any Document 🔁

This pattern can work for a school book, a recipe folder, a company handbook, or a user manual.

### The universal pattern

```python
# 1. Read a document
pages = loader.load()

# 2. Cut it into searchable pieces
chunks = splitter.split_documents(pages)

# 3. Turn pieces into meaning numbers and save them
store = FAISS.from_documents(chunks, embeddings)

# 4. Find pieces related to the question
retriever = store.as_retriever(search_kwargs={"k": 4})
context = retriever.invoke(question)

# 5. Ask the AI to answer only from those pieces
answer = llm.invoke({"question": question, "context": context})
```

### Customize it in 5 ways 🎨

| Use case | Change this |
|---|---|
| 📚 School textbook | Replace the PDF with a textbook PDF |
| 🍰 Recipe helper | Load recipe files and ask about ingredients |
| 🏢 Employee handbook | Index company rules and policies |
| 🛠️ Product manual | Let users ask how to fix or use a device |
| 🧪 Research assistant | Load papers and use deep mode for wider searching |

### Pattern checklist ✅

- [ ] Choose a clean document.
- [ ] Load the document.
- [ ] Split it into useful chunks.
- [ ] Create embeddings.
- [ ] Save and reuse the search index.
- [ ] Pick how many chunks to retrieve.
- [ ] Tell the AI to use only the supplied context.
- [ ] Add conversation memory when follow-up questions matter.
- [ ] Test questions whose answers are both inside and outside the document.

### Production tips 🚀

- Keep the PDF path in a setting instead of hard-coding it.
- Give each document its own index folder.
- Check that the document changed before reusing an old index.
- Store session data safely if many people use the app.
- Add page numbers and source names to every answer.
- Log failures without saving private questions in plain text.
- Add tests for empty PDFs, missing files, and unknown questions.
- Pin package versions for repeatable installs.

### Real-world applications 🌍

1. Customer-support question answering 💬
2. School and university study helpers 🎓
3. Company policy assistants 🏢
4. Medical research document search 🧪
5. Legal document review ⚖️
6. Technical manuals and repair guides 🔧

### The magic formula ✨

> **Document + meaning map + relevant pieces + careful prompt + memory = helpful document chatbot**

The AI does not need to memorize every page. It only needs to be shown the best little pieces at the right moment. 🎯

## Running the Project ▶️

### 1. Install the packages

```bash
pip install -r requirements.txt
```

### 2. Prepare the local chat model

Install and run Ollama, then download the model used by the code:

```bash
ollama pull llama3.2:3b
```

The embedding model may also download the first time it runs, so the first launch can take longer. ⏳

### 3. Start the chatbot

```bash
python project.py
```

### 4. Use it

1. Type your name.
2. Choose `chat` or `deep`.
3. Ask a question about the PDF.
4. Ask more follow-up questions.
5. Type `quit` when finished.

## Before-and-After Example 💬

**Before:**

```text
I need to know something from a long book.
I search and search... 😵
```

**After:**

```text
Please enter your name: Arya
select the mode: chat
enter your question: Who is this story about?
BOT: [An answer based on the matching PDF text]
```

## Fun Facts 🎉

- 🧠 The computer does not search only for matching words; embeddings help it search for related meaning.
- ⚡ The saved FAISS index is like a shortcut through the book.
- 🔬 Deep mode looks at twice as many chunks as chat mode.
- 🗣️ The chatbot can remember earlier messages for the current session.
- 🧊 The model is set to temperature `0`, which encourages steady, less-random answers.
- 🐉 The program can say “I don't know” when the document does not contain the answer.
- 📄 The current code is built for `Game of thrones.pdf`, but the same pattern can use many kinds of documents.

## Important Note About Citations 📝

The project requirements mention showing page numbers, source filenames, and similarity scores after every answer. The current code retrieves document chunks but does not yet print those citations. Adding citation formatting would be a useful next upgrade.

## Summary in 30 Seconds ⏱️

This project makes a friendly robot that answers questions about a PDF. 🤖 It breaks the PDF into pieces, gives each piece a meaning-map number, and saves those numbers in FAISS. When you ask a question, it finds nearby pieces and gives them to Ollama. You can choose quick `chat` mode or wider `deep` mode. The robot remembers your conversation and prints a small report at the end. 📚✨

**One sentence:** Give the robot a document, ask a question, and let it find the right page-sized clues for you. 🚀
