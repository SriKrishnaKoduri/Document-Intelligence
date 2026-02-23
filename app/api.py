from fastapi import APIRouter
from app.schemas import AskRequest, AskResponse
from app.retriever import retrieve
from app.guardrails import validate
from app.generator import generate_answer    

router = APIRouter()

def create_routes(vector_store):

    @router.post("/ask-recruiter", response_model=AskResponse)
    def ask(request: AskRequest):

        results = retrieve(request.question, vector_store)

        if not validate(results):
            return AskResponse(
                answer="Information not found in internal documents.",
                confidence="low",
                source_documents=[],
                similarity_score=0.0
            )

        answer = generate_answer(results)

        return AskResponse(
            answer=answer,
            confidence="high",
            source_documents=[results[0]["source"]],
            similarity_score=results[0]["score"]
        )

    return router