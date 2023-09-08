import json
import aiohttp
import quart
import quart_cors
from quart import request

// app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

hubcart_url = "https://members.app.hubcart.ai:7860/sdapi/v1/txt2img"

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "steps": 20,
        "width": 512,
        "height": 512
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(hubcart_url, headers=headers, json=data) as response:
            if response.status == 200:
                response_json = await response.json()
                image_url = response_json["data"][0]["url"]
                return {"image_url": image_url}
            else:
                return None

@app.post("/images/generations")
async def handle_image_generation():
    try:
        data = await request.json
        prompt = data.get("prompt")

        if prompt:
            design_info = await create_design(prompt)
            if design_info:
                return quart.Response(response=json.dumps(design_info), status=200)
            else:
                return quart.Response(response="Failed to create the design", status=500)
        else:
            return quart.Response(response="No Prompt", status=400)
    except Exception as e:
        return quart.Response(response="Error occurred during API call: " + str(e), status=500)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

@app.get("/legal.html")
async def serve_legal_html():
    try:
        with open("legal.html") as f:
            text = f.read()
            return quart.Response(text, mimetype="text/html")
    except FileNotFoundError:
        return quart.Response(response="Legal page not found", status=404)

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
