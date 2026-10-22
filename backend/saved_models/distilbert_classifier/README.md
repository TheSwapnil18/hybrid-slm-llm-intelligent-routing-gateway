# Fine-Tuned DistilBERT Model Directory

Place the extracted contents of `distilbert_classifier.zip` from Google Colab into this directory.

Expected files:
- `config.json`
- `model.safetensors` (or `pytorch_model.bin`)
- `tokenizer_config.json`
- `vocab.txt`
- `special_tokens_map.json`

Once placed here, set:
```env
CLASSIFIER_MODE=distilbert
```
in your `.env` file to activate the fine-tuned DistilBERT complexity router.
