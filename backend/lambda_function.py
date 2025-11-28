import json
from agent import app

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_question = body.get('question', '')
    except Exception:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid JSON Format")
        }    
    
    if not user_question:
        return {
            'statusCode': 400,
            'body': json.dumps("Field 'question' is required.")
        }

    inputs = {"question": user_question}
    result = app.invoke(inputs)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "answer": result.get("answer", "No answer generated."),
        })
    }