from clarification import ClarificationResult
class ClarificationResult(BaseModel):
    needs_clarification:bool
    question:str | None=None