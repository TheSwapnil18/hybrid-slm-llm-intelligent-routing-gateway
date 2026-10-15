import os
import csv
import sys

# Ensure backend package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.classifier import calculate_complexity

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "training_prompts.csv")

# 130 Sample Prompts covering diverse simple and complex query types
SAMPLE_DATA = [
    # --- SIMPLE / CASUAL CHAT & GREETINGS (Category: chat) ---
    ("Hello there! How are you doing today?", "chat"),
    ("Good morning, have a great day ahead!", "chat"),
    ("Hi, what is your name?", "chat"),
    ("Tell me a funny dad joke.", "chat"),
    ("Who created you?", "chat"),
    ("How is the weather today?", "chat"),
    ("Tell me a knock knock joke.", "chat"),
    ("Are you an artificial intelligence?", "chat"),
    ("Thank you very much for your help!", "chat"),
    ("What's up?", "chat"),
    ("Can you say hello in French?", "chat"),
    ("Give me a random compliment.", "chat"),
    ("Good evening!", "chat"),
    ("What are you capable of?", "chat"),
    ("Bye bye, see you later!", "chat"),

    # --- SIMPLE / FACTUAL & TRIVIA (Category: factual) ---
    ("What is the capital of France?", "factual"),
    ("Who was the first person to walk on the moon?", "factual"),
    ("What is the largest ocean on Earth?", "factual"),
    ("Who painted the Mona Lisa?", "factual"),
    ("What is the boiling point of water in Celsius?", "factual"),
    ("How many continents are there on Earth?", "factual"),
    ("What is the chemical formula for water?", "factual"),
    ("Which planet is closest to the Sun?", "factual"),
    ("Who wrote Romeo and Juliet?", "factual"),
    ("In which country are the pyramids of Giza?", "factual"),
    ("What is the national animal of India?", "factual"),
    ("Who discovered gravity?", "factual"),
    ("What is the tallest mountain in the world?", "factual"),
    ("How many days are in a leap year?", "factual"),
    ("What currency is used in Japan?", "factual"),

    # --- SIMPLE / BASIC DEFINITIONS & LISTS (Category: basic_qa) ---
    ("Define photosynthesis in one sentence.", "basic_qa"),
    ("What is an API?", "basic_qa"),
    ("List five healthy fruits.", "basic_qa"),
    ("Is a tomato a fruit or a vegetable?", "basic_qa"),
    ("What does CPU stand for?", "basic_qa"),
    ("Give me three benefits of drinking water.", "basic_qa"),
    ("What is the difference between RAM and ROM?", "basic_qa"),
    ("Name three renewable energy sources.", "basic_qa"),
    ("What is HTML used for?", "basic_qa"),
    ("What is the primary function of the heart?", "basic_qa"),
    ("Give me a quick recipe for scrambled eggs.", "basic_qa"),
    ("What is an operating system?", "basic_qa"),
    ("List 4 primary colors in art.", "basic_qa"),
    ("What is a noun in English grammar?", "basic_qa"),
    ("What is the speed of light in vacuum?", "basic_qa"),

    # --- SIMPLE / SHORT MATH & CONVERSIONS (Category: basic_math) ---
    ("What is 15 + 27?", "basic_math"),
    ("What is 10 times 8?", "basic_math"),
    ("How many inches are in a foot?", "basic_math"),
    ("Convert 100 kilometers to miles.", "basic_math"),
    ("What is 50 percent of 200?", "basic_math"),
    ("What is 144 divided by 12?", "basic_math"),
    ("What is the square root of 64?", "basic_math"),
    ("How many minutes are in 3 hours?", "basic_math"),
    ("Convert 5 kilograms to pounds.", "basic_math"),
    ("What is 9 squared?", "basic_math"),

    # --- SIMPLE / GENERAL ADVICE (Category: general) ---
    ("Give me 3 tips to wake up early.", "general"),
    ("Suggest a good book for beginners to read.", "general"),
    ("How can I improve my typing speed?", "general"),
    ("What are some good indoor plants?", "general"),
    ("Give me a simple stretching routine.", "general"),
    ("What should I pack for a weekend trip?", "general"),
    ("How to keep my room organized?", "general"),
    ("Tips for drinking more water daily.", "general"),
    ("How to stay focused while studying?", "general"),
    ("What is a good gift for a friend?", "general"),

    # --- COMPLEX / CODING & SOFTWARE ENGINEERING (Category: coding) ---
    ("Write code in Python to implement a binary search tree with insert, delete, and find methods.", "coding"),
    ("Write code for a neural network from scratch using numpy with forward pass and backpropagation.", "coding"),
    ("Write a complete FastAPI microservice that connects to PostgreSQL using async SQLAlchemy with CRUD routes.", "coding"),
    ("Implement the Dijkstra shortest path algorithm in C++ using a priority queue.", "coding"),
    ("Write a React custom hook for handling infinite scroll pagination with debounced scroll listeners.", "coding"),
    ("Write code in Go to implement a concurrent worker pool using channels and WaitGroups.", "coding"),
    ("Implement a thread-safe LRU Cache in Python with O(1) get and put operations.", "coding"),
    ("Write a Dockerfile and docker-compose.yml file for a production-ready Node.js and Redis application.", "coding"),
    ("Write an SQL query with recursive CTE to traverse an organizational hierarchy tree.", "coding"),
    ("Write code to implement AES-256 encryption and decryption in Java using javax.crypto.", "coding"),
    ("Implement a Red-Black tree rebalancing algorithm in Rust.", "coding"),
    ("Write a Kubernetes StatefulSet manifest for deploying a 3-node MongoDB replica set.", "coding"),
    ("Debug this Python code and fix the memory leak occurring in the generator pipeline.", "coding"),
    ("Write an optimized merge sort algorithm in Python and analyze its space complexity.", "coding"),
    ("Write an asynchronous web scraper in Python using aiohttp and BeautifulSoup with rate limiting.", "coding"),

    # --- COMPLEX / ADVANCED MATH & SCIENCE (Category: advanced_math) ---
    ("Calculate the derivative of f(x) = 3x^2 + 2x - 5 and explain the step by step derivation.", "advanced_math"),
    ("Derive the Schrödinger wave equation for a particle in a one-dimensional infinite potential well.", "advanced_math"),
    ("Calculate the eigenvalues and eigenvectors of a 3x3 Hermitian matrix step by step.", "advanced_math"),
    ("Explain the difference between Rayleigh scattering and Mie scattering in atmospheric optics.", "advanced_math"),
    ("Solve the differential equation dy/dx + 2y = e^(-x) with the initial condition y(0) = 1.", "advanced_math"),
    ("Derive the Navier-Stokes equations from conservation of momentum in fluid mechanics.", "advanced_math"),
    ("Calculate the Fourier transform of a rectangular pulse signal and explain the sinc function output.", "advanced_math"),
    ("Explain quantum entanglement and Bell inequality tests with mathematical formulations.", "advanced_math"),
    ("Calculate the volume of a torus using double integration in cylindrical coordinates.", "advanced_math"),
    ("Explain the mechanism of CRISPR-Cas9 gene editing and potential off-target effects in human therapeutics.", "advanced_math"),

    # --- COMPLEX / MULTI-STEP REASONING & SYNTHESIS (Category: reasoning) ---
    ("First, summarize the plot of Inception. Then, compare its narrative structure to The Matrix.", "reasoning"),
    ("First, identify three major flaws in modern monolithic software architecture. Second, propose a microservices migration plan.", "reasoning"),
    ("First, calculate the compound interest on 10000 at 7 percent for 5 years. Then, compare it to a simple interest investment.", "reasoning"),
    ("Analyze the geopolitical implications of renewable energy adoption in developing nations over the next decade.", "reasoning"),
    ("Compare and contrast Kubernetes vs Docker Swarm in terms of scalability, complexity, and ecosystem adoption.", "reasoning"),
    ("Evaluate the trade-offs between consistency and availability in distributed systems according to the CAP theorem.", "reasoning"),
    ("Synthesize a comprehensive marketing strategy for launching a B2B SaaS platform in European markets.", "reasoning"),
    ("Analyze the historical causes and economic impacts of the 2008 global financial crisis.", "reasoning"),
    ("Compare relational databases with graph databases for social network graph analytics.", "reasoning"),
    ("Evaluate the ethics of autonomous vehicle decision making in unavoidable accident scenarios.", "reasoning"),
    ("Analyze how transformer attention mechanisms overcome the vanishing gradient problem of recurrent neural networks.", "reasoning"),
    ("Synthesize the key findings of recent climate change mitigation reports regarding carbon capture technologies.", "reasoning"),
    ("Compare zero-knowledge proofs with optimistic rollups in Ethereum layer 2 scaling solutions.", "reasoning"),
    ("First, analyze the time complexity of QuickSort in best, average, and worst cases. Then, explain randomized pivoting.", "reasoning"),
    ("Evaluate the architectural differences between RISC-V and ARM processor instruction sets.", "reasoning"),

    # --- COMPLEX / IN-DEPTH TECHNICAL ESSAYS & ARCHITECTURE (Category: technical_depth) ---
    ("Explain the internal memory management and garbage collection mechanisms in the Java Virtual Machine.", "technical_depth"),
    ("Design an end-to-end event-driven architecture for a high-frequency trading platform handling 1M events per second.", "technical_depth"),
    ("Explain how Paxos and Raft consensus algorithms achieve distributed agreement during network partitions.", "technical_depth"),
    ("Analyze the security vulnerabilities in OAuth 2.0 and OpenID Connect implementations and how to prevent token leakage.", "technical_depth"),
    ("Explain how modern GPU architectures execute warp-level parallelism and handle memory coalescing.", "technical_depth"),
    ("Design a scalable distributed file storage system similar to Google File System (GFS) with fault tolerance.", "technical_depth"),
    ("Explain how B-Trees and LSM-Trees differ in disk I/O performance for write-heavy vs read-heavy database workloads.", "technical_depth"),
    ("Analyze the impact of quantum computing algorithms like Shor and Grover on modern RSA and ECC cryptographic standards.", "technical_depth"),
    ("Explain the mathematical foundations of Backpropagation Through Time (BPTT) in Recurrent Neural Networks.", "technical_depth"),
    ("Design a reliable data pipeline architecture for processing petabyte-scale telemetry data using Apache Kafka and Apache Spark.", "technical_depth"),
    ("Explain the differences between optimistic concurrency control and two-phase locking in distributed transaction databases.", "technical_depth"),
    ("Analyze the performance trade-offs between WebAssembly and native JavaScript for compute-intensive browser applications.", "technical_depth"),
    ("Explain how diffusion probabilistic models generate high-fidelity images through reverse Markov chain denoising.", "technical_depth"),
    ("Design an end-to-end CI/CD pipeline with automated vulnerability scanning, blue-green deployments, and canary analysis.", "technical_depth"),
    ("Analyze the role of transformer positional encodings: compare sinusoidal embeddings, learned embeddings, and RoPE.", "technical_depth")
]

def generate_dataset():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    records = []
    simple_count = 0
    complex_count = 0
    
    for idx, (prompt, category) in enumerate(SAMPLE_DATA, 1):
        score = calculate_complexity(prompt)
        # Baseline label: simple (<0.5) vs complex (>=0.5)
        label = "simple" if score < 0.5 else "complex"
        if label == "simple":
            simple_count += 1
        else:
            complex_count += 1
            
        records.append({
            "id": idx,
            "prompt": prompt,
            "category": category,
            "heuristic_score": f"{score:.2f}",
            "label": label
        })

    # Write to CSV
    fieldnames = ["id", "prompt", "category", "heuristic_score", "label"]
    with open(OUTPUT_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print("=" * 60)
    print("  TRAINING DATASET GENERATION COMPLETE")
    print("=" * 60)
    print(f"Total Prompts Generated: {len(records)}")
    print(f"  - Simple Prompts:  {simple_count}")
    print(f"  - Complex Prompts: {complex_count}")
    print(f"Dataset saved to: {OUTPUT_PATH}")
    print("You can manually inspect and edit this CSV to adjust labels before training.")
    print("=" * 60)

if __name__ == "__main__":
    generate_dataset()
