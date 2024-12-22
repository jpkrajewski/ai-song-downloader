class Provider:
    def __init__(self, api_key: str, prompt_template: str):
        self.prompt_template = prompt_template
        self.api_key = api_key

    def get_songs_from_prompt(self, prompt: str) -> list[str]:
        raise NotImplementedError
