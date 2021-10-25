from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from elasticsearch import AsyncElasticsearch, NotFoundError
#import elasticsearch
from config import API_CONFIG_ELASTICSEARCH_URL_WITH_USER_PASS
from security import get_current_username
from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Depends,Request
from starlette import status

app = FastAPI(
    title="Contact Search API",
    description="API to add new contact, search contacts by name and other attributes",
    version="1.0.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = AsyncElasticsearch(
    [API_CONFIG_ELASTICSEARCH_URL_WITH_USER_PASS],
    verify_certs=True,
)

async def search(index: str, car: str, place: str):
    if not es:
        logger.warning("Elasticsearch not initialized")
        return None

    try:
        if not (
            results := await es.search(
                index=index,
                body={"query": {
                        "bool": {
                        "must": [],
                        "filter": [
                            {
                            "bool": {
                                "filter": [
                                {
                                    "multi_match": {
                                    "type": "best_fields",
                                    "query": place,
                                    "lenient": True
                                    }
                                },
                                {
                                    "match_phrase": {
                                        "doc.Carmodel": car
                                    }
                                }
                                ]
                            }
                            }
                        ],
                        "should": [],
                        "must_not": []
                        }
                    }},
                size=10,
            )
        ):
            logger.warning("No Search Results")
            return None

        return [
            x["_source"]["doc"] | {"_index": x["_index"], "_id": x["_id"]}
            for x in results["hits"]["hits"]
        ]
    except Exception as e:
        logger.critical("Exception Searching Elasticsearch: " + str(e))
        return None

@app.get("/search/{place}/{car}")
async def search_contact_by_text(
    place: str,
    car: str,
    #username: str = Depends(get_current_username),
):
    #assert username
    index: str = "analystt.*",
    logger.debug(f"{index=}, {id=}")

    if not (results := await search(index=index, place=place, car=car)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Search Results"
        )

    logger.debug(f"{len(results)=}")
    logger.debug(results)

    return results