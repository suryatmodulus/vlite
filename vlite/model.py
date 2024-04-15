import numpy as np
from transformers import AutoModel, AutoTokenizer
import time
import torch
from typing import Dict

class EmbeddingModel:
    def __init__(self, model_name="mixedbread-ai/mxbai-embed-large-v1", device='cpu'):
        start_time = time.time()
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model_metadata = {
            "bert.embedding_length": 512,
            "bert.context_length": 512
        }
        self.embedding_size = self.model_metadata.get("bert.embedding_length", 1024)
        self.context_length = self.model_metadata.get("bert.context_length", 512)
        self.embedding_dtype = "float32"
        end_time = time.time()
        print(f"[model.__init__] Execution time: {end_time - start_time:.5f} seconds")

    def embed(self, texts, precision="binary"):
        if isinstance(texts, str):
            texts = [texts]

        # Tokenization
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt').to(self.device)

        # Forward pass
        with torch.no_grad():
            outputs = self.model(**inputs).last_hidden_state
            # Normalize embeddings across the feature dimension for all tokens
            outputs = torch.nn.functional.normalize(outputs, p=2, dim=2)
            embeddings = outputs[:, 0]  # Use the [CLS] token's embedding after normalization

        if precision == "binary":
            # Optionally reduce dimension to 512 if needed
            embeddings = embeddings[:, :512]  # Slicing the first 512 features if reduction is desired
            # Convert to binary (0 or 1)
            binary_embeddings = (embeddings > 0).byte()
            print("Shape before packing (binary):", binary_embeddings.shape)
            # Convert binary embeddings to numpy and pack bits
            quantized_embeddings = np.packbits(binary_embeddings.cpu().numpy(), axis=-1).astype(np.int8) - 128

            print(f"[model.embed] Quantized embeddings shape: {quantized_embeddings.shape}")
            return quantized_embeddings
        else:
            raise ValueError(f"Unsupported precision: {precision}")
    
    def pooling(self, outputs: torch.Tensor, inputs: Dict,  strategy: str = 'cls') -> np.ndarray:
        if strategy == 'cls':
            pooled_output = outputs[:, 0]
        elif strategy == 'mean':
            attention_mask = inputs["attention_mask"][:, :, None]
            sum_embeddings = torch.sum(outputs * attention_mask, dim=1)
            sum_mask = torch.sum(attention_mask, dim=1)
            pooled_output = sum_embeddings / sum_mask
        else:
            raise NotImplementedError
        return pooled_output

        
    def normalize(self, v: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.normalize(v, p=2, dim=1)

    def token_count(self, text: str) -> int:
        return len(self.tokenizer(text, add_special_tokens=True)['input_ids'])

    def hamming_distance(self, embedding1, embedding2):
        # Calculate Hamming distance directly using bitwise operations
        return np.sum(embedding1 != embedding2, axis=1)

    def search(self, query_embedding, embeddings, top_k):
        embeddings_tensor = torch.from_numpy(embeddings).to(self.device)
        query_embedding_tensor = torch.from_numpy(query_embedding).unsqueeze(0).to(self.device)
        distances = torch.sum(query_embedding_tensor.int() ^ embeddings_tensor.int(), dim=1)
        top_k_indices = torch.topk(distances, top_k, largest=False).indices.cpu().numpy()
        top_k_distances = distances[top_k_indices].cpu().numpy()
        return top_k_indices, top_k_distances