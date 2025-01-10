from typing import List
import requests
import openai
import times
import os
from pydantic import BaseModel

class PerplexityResponse(BaseModel):
    question: str
    response: str
    citations: List[str]

class GPTPrompt:
    @staticmethod
    def generate_related_questions(response: str) -> List[str]:
        prompt = (
            "Generate Related Questions\n\n"
            "**Instructions:**\n"
            "Analyze the following user provided output and generate 5 related questions that delve into its key "
            "concepts, methodologies, comparisons with other approaches, implementation challenges, and potential improvements. "
            "The questions should aim to deepen understanding, explore efficiencies, identify possible enhancements, and consider "
            "practical applications. Response must be one line per question, no numbering or formatting.\n\n"
            f"User Provided Output: {response}"
        )
        
        openai.api_key = os.getenv('OPENAI_API_KEY')

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
            max_tokens=5000
        )
        
        related_questions = response.choices[0].message.content.strip().split("\n")
        return [question.strip() for question in related_questions if question.strip()]

class PerplexityAPI:
    BASE_URL = "https://api.perplexity.ai/chat/completions"
    RATE_LIMIT = 45  # per minute
    TOKEN = os.getenv('PERPLEXITY_API_KEY')

    @staticmethod
    def call_api(message: str) -> PerplexityResponse:
        payload = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "search_recency_filter": "month",
        }
        headers = {
            "Authorization": f"Bearer {PerplexityAPI.TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(PerplexityAPI.BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        choice = data['choices'][0]
        return PerplexityResponse(
            question=message,
            response=choice['message']['content'],
            citations=data.get('citations', [])
        )

class QuestionExplorer:
    def __init__(self, origin_question: str, depth: int = 1):
        self.origin_question = origin_question
        self.depth = depth

    def explore(self, question: str, current_depth: int = 0, history: List[PerplexityResponse] = []) -> List[PerplexityResponse]:

        print(f'calling perplexity Depth: {current_depth} Question: {question}')
        perplexity_response = PerplexityAPI.call_api(question)
        history.append(perplexity_response)

        # Write the response to a file iteratively
        with open('perplexity_related_questions.txt', "a", encoding="utf-8") as file:
            if current_depth == 0:
                file.write(f"Task\n")
                file.write(f"```\n")
                file.write(f"{perplexity_response.question}\n")
                file.write(f"```\n")
                file.write(f"Original Answer\n")
                file.write(f"```\n")
                file.write(f"{perplexity_response.response}\n\n")
                file.write(f"```\n")
            else:
                file.write(f"Additional Research\n")
                file.write(f"```\n")
                #file.write(f"Depth: {current_depth}\n")
                file.write(f"Research Question: {perplexity_response.question}\n")
                file.write(f"Research Answer: {perplexity_response.response}\n")  
                #file.write(f"Citations: {', '.join(perplexity_response.citations)}\n")
                file.write(f"```\n\n")  

        print(f'calling openai related questions')
        related_questions = GPTPrompt.generate_related_questions(perplexity_response.response)
        for related_question in related_questions:
            time.sleep(60 / PerplexityAPI.RATE_LIMIT)  # Respect the rate limit
            if current_depth < self.depth:
                self.explore(related_question, current_depth + 1, history)

        return history

def main() -> None:
    origin_question = """
Thinking step by step refine this concept

### **Step 2: Dynamic Precision Allocation for Token Importance**

Dynamic precision allocation is designed to optimize computational efficiency by assigning different levels of precision (e.g., FP32, FP16, FP8) to tokens, layers, or operations based on their importance during inference. This step ensures that critical tokens or computations are handled with higher precision while less important ones use lower precision, reducing overall compute and memory usage without compromising output quality.

Below is a precise developer design specification for implementing dynamic precision allocation.

---

#### **1. Input Preprocessing**
- **Objective**: Identify tokens or layers that require higher precision based on their importance in the context of the task.
- **Steps**:
  1. Tokenize the input sequence using a pre-trained tokenizer.
  2. Assign initial importance scores to each token based on:
     - Position in the sequence (e.g., tokens near the beginning or end of a sentence often carry more semantic weight).
     - Part-of-speech tagging (e.g., nouns, verbs, and adjectives are typically more important than determiners or conjunctions).
     - Attention scores from the model's self-attention mechanism (computed during forward passes).
     - Frequency-based heuristics (e.g., rare words often carry more information than common ones).

---

#### **2. Precision Assignment Strategy**
- **Objective**: Dynamically assign precision levels to tokens, layers, or operations based on their computed importance scores.
- **Steps**:
  1. **Define Precision Tiers**:
     - Tier 1: High precision (FP32) for critical tokens or layers.
     - Tier 2: Medium precision (FP16) for moderately important tokens or layers.
     - Tier 3: Low precision (FP8) for unimportant tokens or layers.
  2. **Set Thresholds**:
     - Define thresholds for token importance scores to classify them into the above tiers.
       - Example: Importance score > 0.8 → Tier 1; 0.5–0.8 → Tier 2; < 0.5 → Tier 3.

---

#### **3. Token Importance Scoring**
- **Objective**: Compute token-level importance scores dynamically during inference.
- **Steps**:
  1. Use the model's attention mechanism to compute attention weights for each token across all layers.
     - Aggregate attention weights across heads and layers to compute a global importance score for each token:
       $$
       \text{Importance}(t_i) = \frac{1}{L} \sum_{l=1}^{L} \frac{1}{H} \sum_{h=1}^{H} \text{AttentionWeight}(t_i, l, h)
       $$
       where $$ L $$ is the number of layers, $$ H $$ is the number of heads, and $$ t_i $$ is the $$ i $$-th token.
  2. Incorporate additional heuristics into the score:
     - Semantic relevance: Use embeddings from intermediate layers to measure similarity between tokens and the input prompt.
     - Contextual rarity: Assign higher scores to rare or unique tokens using pre-computed frequency tables.

---

#### **4. Layer-Wise Dynamic Precision**
- **Objective**: Adjust precision not just at the token level but also at the layer level based on computational needs.
- **Steps**:
  1. Compute layer-wise activation norms during forward passes to identify computationally intensive layers.
     - Layers with higher activation norms are assigned higher precision tiers.
     - Example metric:
       $$
       \text{LayerImportance}(l) = ||\text{Activation}(l)||_2
       $$
       where $$ l $$ represents the layer index.
  2. Dynamically adjust matrix multiplications and other operations in these layers to use appropriate precision.

---

#### **5. Implementation Details**
##### **A. Mixed-Precision Framework**
- Use libraries like NVIDIA’s TensorRT or PyTorch AMP (Automatic Mixed Precision) to implement dynamic precision adjustments efficiently.
- Define custom hooks for forward passes to adjust precision dynamically based on token/layer importance.

##### **B. Token-Level Precision Adjustment**
- During embedding lookups:
  - Store embeddings in multiple formats (e.g., FP32, FP16, FP8).
  - Select the appropriate format dynamically based on token importance scores.

##### **C. Layer-Level Precision Adjustment**
- During forward passes:
  - Dynamically switch between high-precision and low-precision matrix multiplications and activations using conditional logic in custom PyTorch/TF modules.

##### **D. Caching Mechanism**
- Cache token importance scores and layer activation norms during inference to avoid redundant computations in subsequent steps.

---

#### **6. Output Representation**
After applying dynamic precision allocation:
1. Tokens are processed with varying levels of precision based on their importance.
2. The output includes metadata indicating which tokens/layers were processed with which precision tiers for debugging and optimization purposes.

---

### Example Workflow
1. Input: *"Why is water wet?"*
2. Tokenization:
   - Tokens: `["Why", "is", "water", "wet", "?"]`
   - Initial Scores: `[0.7, 0.4, 0.9, 0.8, 0.3]`
3. Precision Assignment:
   - `"water"` → Tier 1 (FP32)
   - `"wet"` → Tier 1 (FP32)
   - `"Why"` → Tier 2 (FP16)
   - `"is"` → Tier 3 (FP8)
   - `"?"` → Tier 3 (FP8)
4. Layer-Wise Adjustment:
   - Layers with high activation norms use FP32; others default to FP16/FP8.
5. Output: Processed embeddings with reduced memory usage and faster computation while preserving critical information.

---

This design ensures that computational resources are focused where they matter most, enabling efficient yet accurate inference for large language models.
"""
    depth = 2

    explorer = QuestionExplorer(origin_question, depth)
    responses = explorer.explore(origin_question)

    # Format combined responses output
    combined_output = "\n\n".join(
        f"Related Question: {response.question}\nResearch: {response.response}\nCitations: {', '.join(response.citations)}"
        for response in responses
    )

    print(combined_output)

if __name__ == "__main__":
    main()
