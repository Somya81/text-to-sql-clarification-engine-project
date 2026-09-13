def needs_clarification(question):
    question=question.lower().strip()
    if question in ["show customers","customers","show customer"]:
        return True
    return False