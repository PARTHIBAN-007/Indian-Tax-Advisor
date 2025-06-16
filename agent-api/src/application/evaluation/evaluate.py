from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import OpenAI

query = "Who founded OpenAI?"
answer = "Elon Musk and Sam Altman"
contexts = ["OpenAI was founded in 2015 by Elon Musk and Sam Altman."]

result = evaluate(
    data=[
        {"question": query, "answer": answer, "contexts": contexts}
    ],
    metrics=[faithfulness, answer_relevancy],
    llm=OpenAI(model="gpt-4")
)

print(result)
