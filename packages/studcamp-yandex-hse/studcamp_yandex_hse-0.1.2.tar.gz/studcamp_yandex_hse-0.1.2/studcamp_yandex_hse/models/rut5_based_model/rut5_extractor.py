import warnings

warnings.filterwarnings("ignore")

from peft import PeftModel
from transformers import T5ForConditionalGeneration, T5Tokenizer


class RuT5Tagger:
    def __init__(self):
        model_path = "sarahai/ruT5-base-summarizer"
        saved_model_dir = "./weights"

        model = T5ForConditionalGeneration.from_pretrained(model_path, device_map="cpu", offload_state_dict=True)
        self.peft_model = PeftModel.from_pretrained(model, saved_model_dir)
        self.tokenizer = T5Tokenizer.from_pretrained(saved_model_dir)

    def extract(self, text: str, top_p: int = 0.9, temperature: float = 0.5):
        tokenized = self.tokenizer(text, padding="longest", truncation=True, max_length=2048, return_tensors="pt")
        output = self.peft_model.generate(
            **tokenized,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
        )
        decoded = set(self.tokenizer.decode(output[0], skip_special_tokens=True).split(";"))
        tags = [tag for tag in decoded if tag != ""]
        return tags
