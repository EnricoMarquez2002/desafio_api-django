from fastapi import HTTPException

def response_message(status_code, message):
    
    return {
        "status": status_code,
        "detail": message
    }

def exception(status, message):
    return HTTPException(status_code=status, detail=message)




