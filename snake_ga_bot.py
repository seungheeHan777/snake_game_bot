"""유전 알고리즘 봇 학습 실행 파일입니다."""

from ga_bot.trainer import train


if __name__ == "__main__":
    best = train()
    print("best weights:", best.weights)

