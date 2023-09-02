import os
import openai
from dotenv import load_dotenv
from time import sleep

# Load OpenAI API key from environment variables
def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

# Create a training file and return its file_id
# The function retries every `retry_interval` seconds in case of an error
def create_training_file(file_path, retry_interval=5):
    while True:
        try:
            # Open the file and attempt to create a training data file
            with open(file_path, "rb") as f:
                training_data = openai.File.create(file=f, purpose='fine-tune')
                return training_data["id"]
        except FileNotFoundError:
            # If file not found, log an error and return None
            print(f"File {file_path} not found.")
            return None
        except Exception as e:
            # Log any other exceptions and retry
            print(f"Error while generating file_id: {e}")
            sleep(retry_interval)

# Create a fine-tuning job and return its job_id
# The function retries every `retry_interval` seconds in case of an error
def create_fine_tuning_job(file_id, model="gpt-3.5-turbo", retry_interval=30):
    while True:
        try:
            # Create a fine-tuning job
            training_job = openai.FineTuningJob.create(training_file=file_id, model=model)
            return training_job["id"]
        except Exception as e:
            # Log exceptions and retry
            print(f"Error while creating training job: {e}")
            sleep(retry_interval)

# Monitor the status of a fine-tuning job until it is complete
def monitor_fine_tuning_job(job_id, check_interval=100):
    while True:
        try:
            # Check the job status
            res = openai.FineTuningJob.retrieve(job_id)
            if res["finished_at"] is not None:
                print("\nJob finished.")
                return
            else:
                # Print a dot for each check, flush to ensure it appears
                print(".", end="", flush=True)
                sleep(check_interval)
        except Exception as e:
            # Log any exceptions and retry
            print(f"\nError while checking job status: {e}")
            sleep(5)

# Main script execution
if __name__ == "__main__":
    # Load API key and validate
    api_key = load_api_key()
    if api_key is None:
        print("API key not found.")
        exit(1)
    openai.api_key = api_key

    # File path for the training data
    file_path = "primed_data.jsonl"

    # Create a training file and get its file_id
    file_id = create_training_file(file_path)
    if file_id is None:
        exit(1)
    print(f"File ID: {file_id}")

    # Wait for the file to be processed by OpenAI
    print("Waiting for file to be processed...")
    sleep(30)  # Adjust this sleep time if needed

    # Create a fine-tuning job and get its job_id
    job_id = create_fine_tuning_job(file_id)
    if job_id is None:
        exit(1)
    print(f"Job ID: {job_id}")

    # Monitor the fine-tuning job until completion
    monitor_fine_tuning_job(job_id)
