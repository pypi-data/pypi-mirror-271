import os
import dotenv
import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from yaspin import yaspin
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

console = Console()
app = typer.Typer()

dotenv.load_dotenv()
OPENAI_API_KEY = "sk-proj-UChO8ZhGjmIf5aWT2n0AT3BlbkFJ7sJRX8uV9XWDguNOjv6w" 


def chat_bot(question):
    model = ChatOpenAI(
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-4-turbo"
    )

    prompt_template = """
    <|start_header_id|>user<|end_header_id|>
    You are an assistant for answering questions, in Spanish.
    Provide a conversational answer.

    query_text: {question}
"""

    prompt = PromptTemplate(
        input_variables=["question"],
        template=prompt_template
    )

    chat_chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chat_chain.invoke(question)


@app.command()
def main():
    while True:
        user_input = typer.prompt("Mensaje")
        if user_input.lower() in ["/exit", "/bye"]:
            raise typer.Exit()
        else:
            spinner = yaspin(text="Generando respuesta...")
            spinner.start()
            response = Panel(chat_bot(
                f"Please response these questions: {user_input}"))
            # response = Panel(chat_mistral(user_input))
            spinner.stop()
            print(response)


if __name__ == "__main__":
    app()
