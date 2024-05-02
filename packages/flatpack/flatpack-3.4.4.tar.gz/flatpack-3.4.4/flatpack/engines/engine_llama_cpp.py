# llama_cpp.py
from llama_cpp import Llama


class LlamaCPPEngine:
    def __init__(self, repo_id, filename, n_ctx=4096, n_threads=8, verbose=False):
        self.repo_id = repo_id
        self.filename = filename
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.verbose = verbose
        self.model = None

    def load_model(self):
        if self.model is None:
            self.model = Llama.from_pretrained(
                repo_id=self.repo_id,
                filename=self.filename,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                temp=1.0,
                repeat_penalty=1.0,
                verbose=self.verbose
            )
            print("Model loaded successfully.")

    def generate_response(self, context, question):
        self.load_model()
        prompt = f"Context: {context} \nQuestion: {question}\nPlease provide your response in one complete sentence."
        output = self.model(
            f"\n{prompt}\n",
            max_tokens=256,
            stop=[""],
            echo=False
        )
        return output['choices'][0]['text']
