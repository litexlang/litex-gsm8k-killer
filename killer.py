"""verifier.py

Verification utility using multiple LLMs to check if LaTeX code solves a given topic.
"""

from utils.http_utils import get_example_list
from volcenginesdkarkruntime import Ark
import pylitex
import re
from utils.config_utils import get_info


VOLCENGINE_API_KEY = get_info("volcengine_info")["api_key"]


def _prompt_generator(example_list: list[dict[str, str]], row: dict[str, str]) -> str:
    """
    Generate a prompt to verify if the LaTeX code solves the given topic.

    :param example_list: A list of example dictionaries with 'description' and 'solution' keys.
    :param row: A dictionary containing 'description' and 'solution' keys.
    :return: A formatted prompt string.
    """
    examples = "".join(
        f"Title:\n{ex['title']}\n\nQuestion:\n{ex['description']}\n\nCode:\n```\n{ex['solution']}\n```\n\n"
        for ex in example_list
    )
    title = row["title"]
    question = row["description"]
    return f"""
    You are a helpful code snippet.

    Learn from the following Examples:
    {examples}

    If you meet fractions in Question, transform them into decimal numbers if it can be done.
    Now, here is the question you need to answer:

    Title:
    {title}

    Question:
    {question}

    Give me the final Code text only.
    """.strip()


def killer(
    row: dict[str, str], show_false_answers: bool = True
) -> dict[str, str | None]:
    """
    Verify if the LaTeX code solves the given topic using multiple LLMs and majority voting.

    :param row: A dictionary containing 'description', 'solution', and 'expect' keys.
    :return: A dictionary with the original data and the verification results.
    """
    prompt = _prompt_generator(example_list=get_example_list(), row=row)
    client = Ark(api_key=VOLCENGINE_API_KEY, timeout=1800)
    resp_deepseek_r1 = client.chat.completions.create(
        model="deepseek-r1-250528",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    pattern = r"```(?!claim:).*$"
    answer_deepseek_r1 = re.sub(pattern, "", resp_deepseek_r1.choices[0].message.content, flags=re.MULTILINE).strip()  # type: ignore

    if pylitex.run(answer_deepseek_r1)["success"]:
        print(f"Solution verified by Litex.\t{row['id']}")
        return {
            "task_id": row["id"],
            "solution": answer_deepseek_r1,
        }
    else:
        print(f"Solution NOT verified by Litex.\t{row['id']}")
        if show_false_answers:
            print(answer_deepseek_r1)
        return {
            "task_id": row["id"],
            "solution": None,
        }
