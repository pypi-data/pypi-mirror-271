class ModelResponse:

    def __init__(self, answer=None, session_id=None):
        self.answer = answer
        self.session_id = session_id


   
    def create_response(self):
        return {"answer": self.answer, "session_id": self.session_id}