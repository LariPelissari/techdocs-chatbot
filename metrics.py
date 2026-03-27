import time
from chatbot import answer

tests = [
    "Como redefinir senha?",
    "Qual o horário de atendimento?",
    "Qual o endpoint da API?"
]

correct = 0
total = len(tests)

for t in tests:
    start = time.time()
    response = answer(t)
    elapsed = time.time() - start

    print("Pergunta:", t)
    print("Tempo:", elapsed)
    print("Resposta:", response)
    print("-------------------")

    if len(response) > 50:
        correct += 1

accuracy = (correct / total) * 100

print("Taxa de acerto:", accuracy)