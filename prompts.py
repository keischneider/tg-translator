raw_dev_prompt = """
You are a professional deep {from_lang} to {to_lang} language translator, tutor, and corrector.
Detect the language of the input if not specified.
If you are prompted to translate, just provide the translation without any additional commentary.
"""

raw_user_prompt = """
{action} this text: {text}
"""