import json
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="enrich")
@app.route(route="enrich", auth_level=func.AuthLevel.ANONYMOUS)
def enrich(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    out = {"values": []}

    for record in body.get("values", []):
        record_id = record["recordId"]
        text = (record.get("data", {}).get("text") or "")
        try:
            words = len(text.split())
            out["values"].append({
                "recordId": record_id,
                "data": {
                    "wordCount": words,
                    "readingMinutes": round(words / 200, 1)
                },
                "errors": [],
                "warnings": []
            })
        except Exception as ex:
            out["values"].append({
                "recordId": record_id,
                "data": {},
                "errors": [{"message": f"enrich failed: {ex}"}],
                "warnings": []
            })

    return func.HttpResponse(
        body=json.dumps(out),
        mimetype="application/json",
        status_code=200
    )
