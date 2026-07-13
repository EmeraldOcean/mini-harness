from agent import run

def main():
  while True:
    user_input = input("사용자 입력 >> ")

    if user_input == "exit":
      print("프로그램을 종료합니다.")
      break
    response = run(user_input)
    print("Assistant >>", response)

if __name__ == "__main__":
  main()