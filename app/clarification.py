from pydantic import BaseModel
class ClarificationResult(BaseModel):
    needs_clarification:bool
    question:str | None=None