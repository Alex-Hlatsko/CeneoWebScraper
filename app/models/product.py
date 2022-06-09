from flask.globals import request
import requests
import json
from bs4 import BeautifulSoup
from app.utils import extractComponent
from app.models.opinion import Opinion

class Product:
    def __init__(self, productId, productName=None, opinions=[]) -> None:
        self.productId = productId
        self.productName = productName
        self.opinions = opinions.copy()

    def extractName(self):
        respons = requests.get(
            "https://www.ceneo.pl/{}#tab=reviews".format(self.productId))
        if respons.status_code == requests.codes.ok:
            pageDOM = BeautifulSoup(respons.text, 'html.parser')
            self.productName = extractComponent(pageDOM, '.js_product-h1-link')

    def extractProduct(self):
        respons = requests.get("https://www.ceneo.pl/{}#tab=reviews".format(self.productId))
        page = 2
        while respons:
            pageDOM = BeautifulSoup(respons.text, 'html.parser')
            opinions = pageDOM.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extractOpinion(opinion).transformOpinion())
            respons = requests.get(
                "https://www.ceneo.pl/{}/opinie-".format(self.productId)+str(page), allow_redirects=False)
            if respons.status_code == 200:
                page += 1
            else:
                break

    def exportProduct(self):
        with open(f"app/products/{self.productId}.json", "w", encoding="UTF-8") as f:
            json.dump(self.toDict(), f, indent=4, ensure_ascii=False)

    def importProduct(self):
        with open(f"app/products/{self.productId}.json", "r", encoding="UTF-8") as f:
            product = json.load(f)
            self.productName = product['productName']
            opinions = product['opinions']
            for opinion in opinions:
                self.opinions.append(Opinion(**opinion))

    def toDict(self):
        return {
            "productId": self.productId,
            "productName": self.productName,
            "opinions": [opinion.toDict() for opinion in self.opinions]
        }

    def __str__(self) -> str:
        return f"productId: {self.productId}<br>productName: {self.productName}<br>opinions<br><br>" + "<br><br>".join(str(opinion) for opinion in self.opinions)

    def __repr__(self) -> str:
        return f"Product(productId={self.productId}, productName={self.productName}, opinions=[" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])"