from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user, get_trace_handler
from app.services.langchain_service import chain

router = APIRouter()

@router.post("/chat/")
async def quick_response(question: str, user=Depends(get_current_user), handler=Depends(get_trace_handler)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    query = {"question": question, "name": user.username}
    result = await chain.ainvoke(query, config={"callbacks": [handler]})
    return result
