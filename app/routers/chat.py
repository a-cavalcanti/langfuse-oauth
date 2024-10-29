from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user, get_trace_handler
from app.services.langchain_service import chain

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/chat")
async def quick_response(
    question_request: QuestionRequest,  # Agora recebemos um objeto JSON
    user=Depends(get_current_user),
    handler=Depends(get_trace_handler)
):
    print(f"question_request=={question_request}")
    print(f"question_request.question=={question_request.question}")
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated"
        )
    query = {"question": question_request.question, "name": user.username}  # Extrai a pergunta do JSON
    result = await chain.ainvoke(query, config={"callbacks": [handler]})
    return {"text": result}
