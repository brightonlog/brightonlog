import urllib.request
import xml.etree.ElementTree as ET

# 예린님 티스토리 주소
url = 'https://attention-is-all-i-need.tistory.com/rss'

# 로봇이 아닌 일반 사람인 척, 크롬 브라우저로 위장하기
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
req = urllib.request.Request(url, headers=headers)

try:
    # 데이터 가져오기
    response = urllib.request.urlopen(req)
    xml_data = response.read()

    # XML 파싱해서 최근 글 5개 가져오기
    root = ET.fromstring(xml_data)
    posts = []
    for item in root.findall('.//item')[:5]:
        title = item.find('title').text
        link = item.find('link').text
        posts.append(f"- [{title}]({link})")

    posts_text = "\n".join(posts)

    # 기존 README.md 파일 읽어오기
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_text = f.read()

    # 글 목록을 넣을 위치 찾기
    start_marker = ""
    end_marker = ""

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        # 기존 내용 사이에 새로운 글 목록 끼워넣기
        new_readme = readme_text[:start_idx + len(start_marker)] + "\n" + posts_text + "\n" + readme_text[end_idx:]
        
        # 덮어쓰기
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_readme)
        print("README 업데이트 성공!")
    else:
        print("README에서 TISTORY-LIST 태그를 찾을 수 없어요.")

except Exception as e:
    print(f"에러가 발생했어요: {e}")
