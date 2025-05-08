import requests
import json

# Configuration
base_url = "https://kimcartoon.si"
ajax_endpoint = f"{base_url}/ajax/anime/load_episodes_v2"
episode_id = "5758"
server = "hserver"  # Try 'tserver', 'vhserver', or 'hserver'
php_session_id = "04chansniq7vriobsbq9u9lim4"
cf_clearance = "3S1IOKM9EE2wKq.3vPlInA0m0mnvHUZ1P5yueMQ_YTg-1746686770-1.2.1.1-NqMYB0UpihLB8eWBiExJqSSyAX5A8kR1UYyYcXQOcjzNAAzfHa2LzU3QcWxs3VmB_mRh0Od6_GTqgqCHmliclaT999Xog0tc4P9TgUhmJmOSiQsrw910WyVeTTLOJ4dbeQ5shV1HmSC0C_mPATARhm2Mqm76mTwDH8oR7UomQLYvejvmImmqKqWg9kFrn08kIQaJ4Phl3kyHqeDfq3d577Bii2mU4DUbt0F.fbiwsNKt_JWfT0EglrPPzFew4fGfPe9D7LQ6E6G3KgRgTnKeS_NDwmsdZPeQoECXNzHI_rFO8GaKTfX.48xDnSZIaAgjh4ecPqo9rK95lKVzprV0cS3h7mAWvVyI72vAQWL_hF0"

# Headers to mimic the browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Referer": "https://kimcartoon.si/Cartoon/Ben-10-Omniverse.94243/Season-01-Episode-008?id=2875",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Sec-CH-UA": '"Not.A/Brand";v="99", "Chromium";v="136"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"macOS"',
}

# Cookies
cookies = {
    "PHPSESSID": php_session_id,
    "cf_clearance": cf_clearance,
}

# Payload for the AJAX request
payload = {
    "episode_id": episode_id,
}

# Make the AJAX request
try:
    response = requests.post(
        f"{ajax_endpoint}?s={server}",
        headers=headers,
        cookies=cookies,
        data=payload,
        timeout=10
    )
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the JSON response
    data = response.json()

    # Check if the request was successful
    if data.get("status"):
        # Extract the video link
        if data.get("html5"):
            # HTML5 video link (direct MP4 or HLS)
            video_link = data.get("value")
            if video_link:
                print(f"Direct Media Link: {video_link}")
            else:
                print("No direct video link found in 'value'.")
        elif data.get("fb"):
            # Facebook-hosted video
            video_link = data.get("fb") + "#" + data.get("value")
            print(f"Facebook Video Link: {video_link}")
        elif data.get("embed"):
            # Embedded video (e.g., iframe)
            print(f"Embedded Video HTML: {data.get('value')}")
        else:
            print("Unknown video link format.")
        
        # Check for download links (optional)
        if data.get("download_get"):
            download_response = requests.get(data["download_get"], headers=headers, cookies=cookies)
            download_data = download_response.json()
            if download_data.get("playlist"):
                download_link = download_data["playlist"][0]["file"]
                print(f"Download Link: {download_link}")
    else:
        print("Request failed. Response:", data)

except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
