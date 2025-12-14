import torch
import yaml
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-base"


with open("config/lora.yaml") as f:
    lora_cfg = yaml.safe_load(f)
    # Adapter la clé lora_r -> r si présente
    if "lora_r" in lora_cfg:
        lora_cfg["r"] = lora_cfg.pop("lora_r")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

dataset = load_dataset("json", data_files={"train": "data/train.jsonl"})

def format_row(row):
    prompt = f"### Instruction:\n{row['instruction']}\n### Context:\n{row['input']}\n### PHP Code:\n{row['output']}"
    tokens = tokenizer(prompt, truncation=True, padding="max_length", max_length=2048)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

dataset = dataset.map(format_row, remove_columns=dataset["train"].column_names)

model = get_peft_model(model, LoraConfig(**lora_cfg))
model.print_trainable_parameters()

args = TrainingArguments(
    output_dir="outputs",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none"
)

Trainer(model=model, args=args, train_dataset=dataset["train"]).train()
model.save_pretrained("outputs/lora")
