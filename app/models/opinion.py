from app.utils import extractComponent

class Opinion:

    components = {
        "author": ["span.user-post__author-name"],
        "rcmd": ["span.user-post__author-recomendation > em"],
        "stars": ["span.user-post__score-count"],
        "content": ["div.user-post__text"],
        "pros": ["div[class*=\"positives\"] ~ div.review-feature__item", False],
        "cons": ["div[class*=\"negatives\"] ~ div.review-feature__item", False],
        "purchased": ["div.review-pz"],
        "publishDate": ["span.user-post__published > time:nth-child(1)", "datetime"],
        "purchaseDate": ["span.user-post__published > time:nth-child(2)", "datetime"],
        "useful": ["span[id^='votes-yes']"],
        "useless": ["span[id^='votes-no']"]
    }

    def __init__(self, opinionId=None, author=None, rcmd=None, stars=None, content=None, pros=None, cons=None, purchased=None, publishDate=None, purchaseDate=None, useful=None, useless=None) -> None:
        self.opinionId = opinionId
        self.author = author
        self.rcmd = rcmd
        self.stars = stars
        self.content = content
        self.pros = pros
        self.cons = cons
        self.purchased = purchased
        self.publishDate = publishDate
        self.purchaseDate = purchaseDate
        self.useful = useful
        self.useless = useless
    
    def extractOpinion(self, opinion):
        for key, value in self.components.items():
            setattr(self, key, extractComponent(opinion, *value))
        self.opinionId = opinion["data-entry-id"]
        return self

    def transformOpinion(self):
        self.rcmd = True if self.rcmd == "Polecam" else False if self.rcmd == "Nie polecam" else self.rcmd
        self.stars = float(self.stars.split("/")[0].replace(",", "."))
        self.content = self.content.replace("\n", " ").replace("\r", " ")
        self.purchased = bool(self.purchased)
        self.useful = int(self.useful)
        self.useless = int(self.useless)
        return self

    def toDict(self):
        return {"opinionId": self.opinionId} | {key: getattr(self, key) for key in self.components.keys()}

    def __str__(self) -> str:
        return f"opinionId: {self.opinionId}<br>" + "<br>".join(f"{key}: {str(getattr(self, key))}" for key in self.components.keys())

    def __repr__(self) -> str:
        return f"Opinion(opinionId={self.opinionId}, " + ", ".join(f"{key}={str(getattr(self, key))}" for key in self.components.keys()) + ")"