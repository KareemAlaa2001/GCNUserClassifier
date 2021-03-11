from transformers import AutoTokenizer, AutoModel  

tokenizer = AutoTokenizer.from_pretrained("lanwuwei/BERTOverflow_stackoverflow_github")  
model = AutoModel.from_pretrained("lanwuwei/BERTOverflow_stackoverflow_github")