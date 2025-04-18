import json

# JSON 문자열을 변수에 저장 (API응답)
json_str = '''{
    "lastBuildDate":"Fri, 18 Apr 2025 15:57:31 +0900",
    "total":90862729,
    "start":1,
    "display":10,
    "items":[
        {
            "title":"xxxxxxxxxx",
            "link":"https://blog.naver.com/yyyyyyyy",
            "description":"zzzzzzzz",
            "bloggername":"aaaaaaaa",
            "bloggerlink":"blog.naver.com/bbbbbbbb",
            "postdate":"20250416"
        },
        {
            "title":"xxxxxxxx",
            "link":"https://..."
        }
    ]
}'''

# 1. JSON 파싱
data = json.loads(json_str)

# 2. items만 추출
items = data["items"]

# 3. 각 항목 출력
for i, item in enumerate(items, 1):
    title = item["title"]
    link = item["link"]
    description = item.get("description", "")
    blogger = item.get("bloggername", "")
    
    print(f"[{i}] 제목: {title}")
    print(f"     링크: {link}")
    print(f"     설명: {description}")
    print(f"     블로거: {blogger}")
    print()
