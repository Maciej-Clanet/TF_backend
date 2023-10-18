from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.dbutils import getArticles
from typing import List, Dict

router = APIRouter()

#they will not get this far feel free to ignore

class Article(BaseModel):
    id: str
    heading: str
    intro: str
    content: str


@router.get("/article/{article_id}", response_model=Article)
def get_article(article_id):
    articles = getArticles()
    print(articles[article_id]["path"])
    
    #find article
    if article_id in articles:
        print(articles[article_id]["path"])
        
        with open(articles[article_id]["path"], "r") as file:
                markdown_content = file.read()

        return {
            "id" : article_id,
            "heading" : articles[article_id]["heading"],
            "intro" : articles[article_id]["intro"],
            "content":markdown_content
        }

    
    raise HTTPException(400, detail="article not found")
