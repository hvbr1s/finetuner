Here's how to use the finetuner:

1. Log all Q&A pairs into `input_data.jsonl`  
2. Run `data_primer.py` to add the `system_promt` to each Q&A and output the final `primed_data.jsonl` file, which will be used for fine-tuning the model.
3. Run `dataformat_checker.py` to ensure `primed_data.jsonl` is error free and to get a cost estimation for the fine-tuning job. 
4. Run `finetuner.py` to start the fine-tuning job.  
5. Once the job is complete, the message "Job finished" will be printed in the console, and you will receive an email from OpenAI with the model ID, which you can incorporate into your app.  

