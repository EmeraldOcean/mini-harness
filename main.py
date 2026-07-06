from agent import run

def main():
  contexts = []
  while True:
    user_input = input("사용자 입력 >> ")
    contexts.append({
      "role":"user",
      "content": user_input
    })
    if user_input == "exit":
      print("프로그램을 종료합니다.")
      break

    response = run(contexts)
    contexts.append({
      "role": "assistant",
      "content": response
    })
    print(response)

if __name__ == "__main__":
  main()