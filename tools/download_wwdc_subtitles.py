import requests

# 下载 WWDC 字幕文件
def download_wwdc_subtitles():
    for counter in range(329):
        url = f"https://devstreaming-cdn.apple.com/videos/wwdc/2024/10173/4/5ADD00F7-AAD5-4C66-A3ED-9FC7E27C7720/subtitles/eng/sequence_{counter}.webvtt"
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"sequence_{counter}.webvtt", "wb") as file:
                file.write(response.content)
            print(f"Downloaded sequence_{counter}.webvtt")
        else:
            print(f"Failed to download sequence_{counter}.webvtt")

# 合并
def merge_subtitles():
    with open("full.webvtt", "wb") as full_file:
        for counter in range(329):
            with open(f"sequence_{counter}.webvtt", "rb") as file:
                full_file.write(file.read())
            print(f"Merged sequence_{counter}.webvtt")

if __name__ == "__main__":
    download_subtitles()
    merge_subtitles()
    print("All subtitle files have been downloaded and merged into full.webvtt")