import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_valid_base_url():
    while True:
        base_url_str = input("Enter the base URL (e.g., https://devstreaming-cdn.apple.com/videos/wwdc/2024/10173/4/xx-xx-xx-xx-xx/subtitles/eng/sequence_0.webvtt): ").strip()
        if base_url_str.endswith(".webvtt"):
            return base_url_str
        else:
            print("The entered URL is incorrect. Ensure it ends with .webvtt. Please try again.")

def get_valid_count(base_url_str):
    while True:
        count_str = input("Enter the total number of subtitle files: ").strip()
        try:
            count = int(count_str)
            if count > 0:
                return count
            else:
                print("The entered total number of subtitle files must be a positive integer. Please try again.")
        except ValueError:
            print(f"The entered total number of subtitle files '{count_str}' is not a valid integer. Please enter a valid number.")

base_url_str = get_valid_base_url()
count = get_valid_count(base_url_str)

base_url_prefix = base_url_str.rsplit("_", 1)[0]

# Download single subtitle file
def download_subtitle(counter):
    url = f"{base_url_prefix}_{counter}.webvtt"
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"sequence_{counter}.webvtt", "wb") as file:
            file.write(response.content)
        print(f"Downloaded sequence_{counter}.webvtt")
        return True
    else:
        print(f"Failed to download sequence_{counter}.webvtt")
        return False

# Concurrent download
def download_subtitles_concurrently(count):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_subtitle, counter) for counter in range(count)]
        for future in as_completed(futures):
            future.result()

# Merge and clean subtitles
def merge_and_clean_subtitles(count):
    with open("full.webvtt", "w", encoding='utf-8') as full_file:
        for counter in range(count):
            with open(f"sequence_{counter}.webvtt", "r", encoding='utf-8') as file:
                content = file.read()
                # Remove timestamp lines, WEBVTT tags, and extra blank lines
                cleaned_content = re.sub(r'(WEBVTT|\n\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})\n', '', content)
                # Replace multiple consecutive newlines with a single newline
                cleaned_content = re.sub(r'\n\s*\n', '\n', cleaned_content)
                full_file.write(cleaned_content)
            print(f"Merged sequence_{counter}.webvtt")

if __name__ == "__main__":
    print(f"Downloading and merging {count} subtitle files from {base_url_prefix}_<index>.webvtt")
    # Concurrently download subtitles
    download_subtitles_concurrently(count)
    # Merge subtitles
    merge_and_clean_subtitles(count)
    print("All subtitle files have been downloaded and merged into full.webvtt")