import requests

# Prompt user to enter the base URL and total number of subtitle files
base_url = input("Enter the base URL (e.g., https://devstreaming-cdn.apple.com/videos/wwdc/2024/10173/4/xx-xx-xx-xx-xx/subtitles/eng/sequence_0.webvtt): ")
count = int(input("Enter the total number of subtitle files: "))

# Confirm the correct ending for the base URL
if not base_url.endswith(".webvtt"):
    print("The entered URL is incorrect. Ensure it ends with .webvtt.")
    exit(1)

base_url_prefix = base_url.rsplit("_", 1)[0]

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
    with open("full.webvtt", "wb") as full_file:
        for counter in range(count):
            with open(f"sequence_{counter}.webvtt", "rb") as file:
                content = file.read()
                # Use regular expressions to remove "WEBVTT" tags and timestamp lines
                cleaned_content = re.sub(rb'WEBVTT\n\n(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n)?', b'',
                                         content)
                full_file.write(cleaned_content)
            print(f"Merged sequence_{counter}.webvtt")

if __name__ == "__main__":
    print(f"Downloading and merging {count} subtitle files from {base_url_prefix}_<index>.webvtt")
    # Concurrently download subtitles
    download_subtitles_concurrently(count)
    # Merge subtitles
    merge_and_clean_subtitles(count)
    print("All subtitle files have been downloaded and merged into full.webvtt")