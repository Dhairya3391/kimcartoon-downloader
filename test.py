import requests

iframe_url = "https://em.vidstream.vip?k=b39f945438bd62fb085d80804071e66a87f2103d75b6640d60792f0098854481acdbdbbd7389a2238702b48bf82985522cc644fb33fdb7bf095a602bce55f445c797b52f9773de2a1e8f1e5cf7710ab18429e80f1e61441f164f58f1c2cc46fa&li=2875&tham=1746686608<=ts&check_hot=1&qlt=720p&spq=p&prv=bWVkaWEvdGh1bWIvMTcwNDA3XzAxMzgvQmVuLTEwLU9tbml2ZXJzZS1TZWFzb24tMDEtRXBpc29kZS0wMDguanBnO21lZGlhL3RodW1iLzE3MDQwN18wMTM4L0Jlbi0xMC1PbW5pdmVyc2UtU2Vhc29uLTAxLUVwaXNvZGUtMDA4X21vYmlsZS5qcGc%3D&key=9ec265ca8e88e1cfe416f0b03f5256be&ua=802a1200e7ca638d6a6071bfed50e66dd9601ba77a61cd5f11804df3c90df3453fc8756844ea4426915362f8d4901f36d4849f99489af54daa8d45f34b80c0793e9c6effd19285e996c192380266c980d995438b2233746fa25449f2c9fb528a605633c8101c3a26c352f2cddd15ecc68b67ee807ea2506644d25c222b23e569&h=1746686608"
headers = {
    "sec-ch-ua-platform": "macOS",
    "sec-ch-ua": '"Not.A/Brand";v="99", "Chromium";v="136"',
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "dnt": "1",
    "origin": "https://kimcartoon.si",
    "referer": "https://kimcartoon.si/Cartoon/Ben-10-Omniverse.94243/Season-01-Episode-008?id=2875",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "priority": "u=0, i"
}
cookies = {
    "uname": "Dhairya3391",
    "PHPSESSID": "6dtvao27ahba8llt5rbrr67837",
    "view-68": "true"
}

response = requests.get(iframe_url, headers=headers, cookies=cookies)
if response.status_code == 200:
    print(response.text)  # Inspect HTML for video sources or JavaScript
else:
    print(f"Request failed: {response.status_code}")