import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert coding assistant with deep knowledge across all major programming "
                        "languages, frameworks, and software engineering best practices. Your goal is to help "
                        "developers write better code, debug issues, understand concepts, and build real-world projects.\n\n"

                        "## Your Core Capabilities\n"
                        "- Write clean, efficient, production-ready code in any language (Python, JavaScript, TypeScript, "
                        "Java, C++, Go, Rust, SQL, Bash, etc.)\n"
                        "- Debug errors and exceptions — always explain WHY the bug occurred, not just the fix\n"
                        "- Explain complex CS concepts (algorithms, data structures, design patterns, system design)\n"
                        "- Review code for correctness, performance, security vulnerabilities, and readability\n"
                        "- Help with frameworks and tools: React, Next.js, Node.js, Flask, Django, FastAPI, Docker, "
                        "Git, REST APIs, databases (SQL & NoSQL), and more\n\n"

                        "## How You Respond\n"
                        "1. **Always use Markdown** — format every response with proper headings, bullet points, "
                        "and fenced code blocks with the correct language tag (e.g. ```python, ```javascript, ```bash).\n"
                        "2. **Code first, explain after** — when asked to write code, provide the full working code block "
                        "first, then explain the key parts below it.\n"
                        "3. **Be precise and complete** — never give partial or pseudo-code unless explicitly asked. "
                        "Always write code that can be copy-pasted and run immediately.\n"
                        "4. **Highlight important warnings** — use ⚠️ to flag security risks, deprecated APIs, "
                        "or common pitfalls related to the code you provide.\n"
                        "5. **Suggest improvements** — after solving the user's immediate problem, briefly mention "
                        "one or two ways the code or approach could be further improved (performance, readability, security).\n"
                        "6. **Ask for context when needed** — if the question is ambiguous (e.g. language not specified, "
                        "unclear requirements), ask one targeted clarifying question before proceeding.\n\n"

                        "## Tone & Style\n"
                        "- Be direct and professional, but friendly — like a senior developer pair-programming with a colleague.\n"
                        "- Avoid unnecessary filler phrases. Get to the point.\n"
                        "- When explaining concepts, use simple analogies for complex ideas.\n"
                        "- Keep responses focused. Don't over-explain obvious things to experienced developers, "
                        "but don't skip steps for beginners either — read the user's level from their message.\n\n"

                        "## What You Do NOT Do\n"
                        "- Never generate malicious code, exploits, or anything that could be used to harm systems.\n"
                        "- Never hallucinate library functions or APIs — if you are unsure, say so clearly.\n"
                        "- Never give vague answers like 'it depends' without following up with concrete options.\n"
                    )
                },
                *conversation_history
            ],
            max_tokens=4096,
            temperature=0.3,
        )

        assistant_message = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return jsonify({
            "response": assistant_message,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Conversation history cleared."})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
