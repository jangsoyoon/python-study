import random


def cook_dumpling():
    cooking_time = random.randint(1, 10)

    print(f"\n🔥 만두를 {cooking_time}초 동안 구웠습니다!")

    if cooking_time < 4:
        print("🥟 아직 덜 익었어요!")
        return 0

    elif cooking_time <= 7:
        print("✨ 노릇노릇! 완벽하게 구워졌어요!")
        return 10

    else:
        print("🔥 만두가 타버렸어요!")
        return -5


def show_result(score):
    print("\n===== 게임 결과 =====")
    print(f"최종 점수: {score}점")

    if score >= 30:
        print("🏆 만두 굽기 장인!")
    elif score >= 10:
        print("😊 꽤 잘 구웠어요!")
    else:
        print("😭 만두를 살려주세요...")


def game():
    score = 0
    count = 0

    print("🥟 만두 굽기 게임을 시작합니다!")

    while count < 5:
        print(f"\n[{count + 1}번째 만두]")

        score += cook_dumpling()
        count += 1

        print(f"현재 점수: {score}점")

    show_result(score)


game()
