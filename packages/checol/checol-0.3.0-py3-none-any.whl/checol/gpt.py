import anthropic


class Claude:
    def __init__(
        self,
        api_key,
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        system="このコード差分を見てプロの目線でコードレビューしてください",
    ):
        self.client = anthropic.Client(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.system = system
        self.messages = []

    def send(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system,
            messages=self.messages,
        )
        content = result.content[0].text
        self.messages.append({"role": result.role, "content": content})
        return result
