from sentence_transformers import SentenceTransformer, util
import os

class RAGService:
    def __init__(self, policy_path="policies.txt"):
        self.policy_path = policy_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.policies = self._load_policies()
        self.embeddings = self.model.encode(self.policies, convert_to_tensor=True)

    def _load_policies(self):
        if not os.path.exists(self.policy_path):
            print(f"Warning: Policy file {self.policy_path} not found.")
            return []
        
        with open(self.policy_path, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines

    def retrieve_context(self, query, top_k=2):
        """
        Retrieves top_k most relevant policies for a given query.
        """
        if not self.policies:
            return ""

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=top_k)
        
        # Format results
        relevant_policies = []
        for hit in hits[0]:
            idx = hit['corpus_id']
            relevant_policies.append(self.policies[idx])
        
        return "\n".join(relevant_policies)

if __name__ == "__main__":
    # Test block
    print("Initializing RAG Service...")
    rag = RAGService()
    print("Searching for 'credit score'...")
    context = rag.retrieve_context("My credit score is 600")
    print(f"Retrieved Context:\n{context}")
