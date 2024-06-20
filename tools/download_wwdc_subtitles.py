import requests

# 提示用户输入基本 URL 和字幕文件的总数
base_url = input("Enter the base URL (e.g., https://devstreaming-cdn.apple.com/videos/wwdc/2024/10173/4/5ADD00F7-AAD5-4C66-A3ED-9FC7E27C7720/subtitles/eng/sequence_0.webvtt): ")
count = int(input("Enter the total number of subtitle files: "))

# 下载 WWDC 字幕文件
def download_subtitles(base_url, count):
    for counter in range(count):
        url = base_url.replace("sequence_0.webvtt", f"sequence_{counter}.webvtt")
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"sequence_{counter}.webvtt", "wb") as file:
                file.write(response.content)
            print(f"Downloaded sequence_{counter}.webvtt")
        else:
            print(f"Failed to download sequence_{counter}.webvtt")


# 合并
def merge_subtitles(count):
    with open("full.webvtt", "wb") as full_file:
        for counter in range(count):
            with open(f"sequence_{counter}.webvtt", "rb") as file:
                full_file.write(file.read())
            print(f"Merged sequence_{counter}.webvtt")


if __name__ == "__main__":
    print(f"Downloading and merging {count} subtitle files from {base_url}")
    download_subtitles(base_url, count)
    # 合并
    merge_subtitles(count)
    print("All subtitle files have been downloaded and merged into full.webvtt")