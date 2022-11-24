import json
import requests


class MyFile():
    def __init__(self, path: str):
        self.path = path

    def read(self) -> list | None:
        with open(self.path, "r") as file:
            return json.load(file)

    def write(self, data) -> None:
        print("[MyFile] Escrevendo no arquivo...")
        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)


def getNewContents(amount: int = 10) -> dict | None:
    print("[APP] Consultando API...")
    url = f"https://www.tabnews.com.br/api/v1/contents?per_page={amount}&strategy=new"
    response = requests.get(url).json()
    responseSorted = sorted(response, key=lambda r: r['published_at'])
    return responseSorted


def getContentDetails(user: str, slug: str) -> dict | None:
    print("[APP] Consultando API...")
    url = f"https://www.tabnews.com.br/api/v1/contents/{user}/{slug}"
    return requests.get(url).json()


def removeMarkdown(text: str) -> str | None:
    dictionary = ['#', '![', '](', '> ']
    for i in dictionary:
        text = text.replace(i, '')
        text = text.replace('\n', ' ')
    return text.strip()


def checkContents():
    writeFile = False
    tempContents = []

    file = MyFile('./JSON/oldContentsIDs.json')
    oldContents = file.read()
    oldContentsIDs = [i["id"] for i in oldContents]
    newContents = getNewContents()

    for content in newContents:
        if content['id'] not in oldContentsIDs:
            contentDetails = getContentDetails(
                content['owner_username'],
                content['slug']
            )
            content['body'] = removeMarkdown(contentDetails['body'])
            tempContents.append(content)
            writeFile = True

    if writeFile:
        data = sorted(oldContents, key=lambda r: r['published_at'])
        for i in tempContents:
            data.append(i)
            data.pop(0)
        file.write(data)

    return tempContents


if __name__ == "__main__":
    ...
