import unittest
import numpy as np
from vlite.main import VLite
import os
from vlite.utils import process_pdf
import time

class TestVLite(unittest.TestCase):
    test_times = {}
    vlite = VLite("vlite-unit")

    def test_add_text(self):
        start_time = time.time()
        text = "This is a test text. " * 100
        metadata = {"source": "test", "author": "John Doe", "timestamp": "2023-06-08"}
        self.vlite.add(text, metadata=metadata, item_id="test_text_1")
        end_time = time.time()
        TestVLite.test_times["add_single_text"] = end_time - start_time
        print(f"Count of texts in the collection: {self.vlite.count()}")

    def test_add_texts(self):
        start_time = time.time()
        text_512tokens = "underreckoning fleckiness hairstane paradigmatic eligibility sublevate xviii achylia reremice flung outpurl questing gilia unosmotic unsuckled plecopterid excludable phenazine fricando unfledgedness spiritsome incircle desmogenous subclavate redbug semihoral district chrysocolla protocoled servius readings propolises javali dujan stickman attendee hambone obtusipennate tightropes monitorially signaletics diestrums preassigning spriggy yestermorning margaritic tankfuls aseptify linearity hilasmic twinning tokonoma seminormalness cerebrospinant refroid doghouse kochab dacryocystalgia saltbushes newcomer provoker berberid platycoria overpersuaded reoverflow constrainable headless forgivably syzygal purled reese polyglottonic decennary embronze pluripotent equivocally myoblasts thymelaeaceous confervae perverted preanticipate mammalogical desalinizing tackets misappearance subflexuose concludence effluviums runtish gras cuckolded hemostasia coatroom chelidon policizer trichinised frontstall impositions unta outrance scholium fibrochondritis furcates fleaweed housefront helipads hemachate snift appellativeness knobwood superinclination tsures haberdasheries unparliamented reexecution nontangential waddied desolated subdistinctively undiscernibleness swishiest dextral progs koprino bruisingly unloanably bardash uncuckoldedunderreckoning fleckiness hairstane paradigmatic eligibility sublevate xviii achylia reremice flung outpurl questing gilia unosmotic unsuckled plecopterid excludable phenazine fricando unfledgedness spiritsome incircle desmogenous subclavate redbug semihoral district chrysocolla spriggy yestermorning margaritic tankfuls aseptify linearity hilasmic twinning tokonoma seminormalness cerebrospinant refroequivocally myoblasts thymelaeaceous confervae perverted preantiest dextral progs koprino bruisingly unloanably bardash uncuckolded"
        metadata = {"source": "test_512tokens", "category": "random"}
        self.vlite.add(text_512tokens, metadata=metadata, item_id="test_text_2")

        with open(os.path.join(os.path.dirname(__file__), "data/text-8192tokens.txt"), "r") as file:
            text_8192tokens = file.read()
        metadata = {"source": "test_8192tokens", "category": "long_text"}
        self.vlite.add(text_8192tokens, metadata=metadata, item_id="test_text_3")

        end_time = time.time()
        TestVLite.test_times["add_multiple_texts"] = end_time - start_time
        print(f"Count of texts in the collection: {self.vlite.count()}")

    def test_add_pdf(self):
        print(f"[test_add_pdf] Count of chunks in the collection: {self.vlite.count()}")
        start_time = time.time()
        self.vlite.add(process_pdf(os.path.join(os.path.dirname(__file__), 'data/attention.pdf')), need_chunks=False, item_id="test_pdf_1")
        end_time = time.time()
        TestVLite.test_times["add_pdf"] = end_time - start_time
        print(f"[test_add_pdf] after Count of chunks in the collection: {self.vlite.count()}")
        print(f"Time to add 71067 tokens: {TestVLite.test_times['add_pdf']} seconds")

    def test_retrieve(self):
        queries = [
            "What is the architecture of GPT-4?",
            "How does GPT-4 handle contextual understanding?",
            "What are the key improvements in GPT-4 over GPT-3?",
            "How many parameters does GPT-4 have?",
            "What are the limitations of GPT-4?",
            "What datasets were used to train GPT-4?",
            "How does GPT-4 handle longer context?",
            "What is the computational requirement for training GPT-4?",
            "What techniques were used to train GPT-4?",
            "What is the impact of GPT-4 on natural language processing?",
            "What are the use cases demonstrated in the GPT-4 paper?",
            "What are the evaluation metrics used in GPT-4's paper?",
            "What kind of ethical considerations are discussed in the GPT-4 paper?",
            "How does the GPT-4 handle tokenization?",
            "What are the novel contributions of the GPT-4 model?"
        ]
        start_time = time.time()
        for query in queries:
            results = self.vlite.retrieve(query, top_k=3)
            print(f"Query: {query}")
            print(f"Top 3 results:")
            for text, similarity, metadata in results[:3]:
                print(f"Text: {text[:100]}...")
                print(f"Similarity: {similarity}")
                print(f"Metadata: {metadata}")
                print("---")
        end_time = time.time()
        TestVLite.test_times["retrieve"] = end_time - start_time

    def test_delete(self):
        self.vlite.add("This is a test text.", item_id="test_delete_1")
        self.vlite.add("Another test text.", item_id="test_delete_2")
        start_time = time.time()
        self.vlite.delete(['test_delete_1', 'test_delete_2'])
        end_time = time.time()
        TestVLite.test_times["delete"] = end_time - start_time
        print(f"Count of texts in the collection: {self.vlite.count()}")

    def test_update(self):
        self.vlite.add("This is a test text.", item_id="test_update_1")
        start_time = time.time()
        self.vlite.update("test_update_1", text="This is an updated text.", metadata={"updated": True})
        end_time = time.time()
        TestVLite.test_times["update"] = end_time - start_time
        print(f"Count of texts in the collection: {self.vlite.count()}")

    def test_get(self):
        self.vlite.add("Text 1", item_id="test_get_1", metadata={"category": "A"})
        self.vlite.add("Text 2", item_id="test_get_2", metadata={"category": "B"})
        self.vlite.add("Text 3", item_id="test_get_3", metadata={"category": "A"})

        start_time = time.time()
        items = self.vlite.get(ids=["test_get_1", "test_get_3"])
        print(f"Items with IDs 'test_get_1' and 'test_get_3': {items}")

        items = self.vlite.get(where={"category": "A"})
        print(f"Items with category 'A': {items}")
        end_time = time.time()
        TestVLite.test_times["get"] = end_time - start_time

    def test_set(self):
        self.vlite.add("Original text", item_id="test_set_1", metadata={"original": True})
        start_time = time.time()
        self.vlite.set("test_set_1", text="Updated text", metadata={"updated": True})
        end_time = time.time()
        TestVLite.test_times["set"] = end_time - start_time

        items = self.vlite.get(ids=["test_set_1"])
        print(f"Updated item: {items}")

    def test_count(self):
        start_time = time.time()
        count = self.vlite.count()
        print(f"Count of items in the collection: {count}")
        end_time = time.time()
        TestVLite.test_times["count"] = end_time - start_time

    def test_clear(self):
        start_time = time.time()
        self.vlite.clear()
        print(f"Count of items after clearing the collection: {self.vlite.count()}")
        end_time = time.time()
        TestVLite.test_times["clear"] = end_time - start_time

    @classmethod
    def tearDownClass(cls):
        print("\nTest times:")
        for test_name, test_time in cls.test_times.items():
            print(f"{test_name}: {test_time:.4f} seconds")
        if os.path.exists('vlite-unit.npz'):
            print("[+] Removing vlite")
            os.remove('vlite-unit.npz')
        if os.path.exists('vlite-unit.omom'):
            print("[+] Removing vlite")
            os.remove('vlite-unit.omom')
        if os.path.exists('omnom/vlite-unit.omom'):
            print("[+] Removing vlite omom")
            os.remove('omnom/vlite-unit.omom')

if __name__ == '__main__':
    unittest.main(verbosity=2)