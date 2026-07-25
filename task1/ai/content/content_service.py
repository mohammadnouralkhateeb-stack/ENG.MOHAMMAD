from ai.content.content_client import ContentClient

def generate_response(prompt):
    if not isinstance(prompt, dict) or not prompt:
        raise ValueError('Prompt must be a non-empty dictionary.')

    title = prompt.get('title')
    tone = prompt.get('tone')

    if not title or not str(title).strip():
        raise ValueError('Title is required.')

    title_clean = str(title).strip()

    if tone and str(tone).strip():
        prompt_text = f"Write a short blog post about {title_clean}, tone: {str(tone).strip()}."
    else:
        prompt_text = f"Write a short blog post about {title_clean}."

    client = ContentClient()
    content = client.generate(prompt_text)

    if not content:
        raise ValueError('Something wrong occurred! Model cannot generate a response.')

    content_clean = content.strip()

    return {
        "title": title_clean,
        "content": content_clean,
        "length": len(content_clean)
    }