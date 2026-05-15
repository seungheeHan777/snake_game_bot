"""유전 알고리즘 학습 결과 저장과 불러오기 코드입니다."""

import csv
import json
from pathlib import Path

from ga_bot.policy import Individual

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
BEST_MODEL_PATH = MODELS_DIR / "best_weights.json"
CHECKPOINT_PATH = MODELS_DIR / "checkpoint.json"
HISTORY_PATH = LOGS_DIR / "training_history.csv"


def ensure_storage_dirs():
    """모델과 로그 저장 폴더를 만듭니다."""
    MODELS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)


def individual_to_dict(individual, generation=None):
    """개체 정보를 JSON으로 저장 가능한 dict로 바꿉니다."""
    data = {
        "weights": individual.weights,
        "fitness": individual.fitness,
        "score": individual.score,
        "steps": individual.steps,
    }
    if generation is not None:
        data["generation"] = generation
    return data


def individual_from_dict(data):
    """저장된 dict에서 개체를 복원합니다."""
    return Individual(
        weights=list(data["weights"]),
        fitness=data.get("fitness", 0),
        score=data.get("score", 0),
        steps=data.get("steps", 0),
    )


def save_best_model(individual, generation):
    """현재까지 가장 좋은 개체를 JSON 파일로 저장합니다."""
    ensure_storage_dirs()
    with BEST_MODEL_PATH.open("w", encoding="utf-8") as file:
        json.dump(individual_to_dict(individual, generation), file, indent=2)


def load_best_model():
    """저장된 최고 개체를 불러옵니다."""
    if not BEST_MODEL_PATH.exists():
        return None
    with BEST_MODEL_PATH.open("r", encoding="utf-8") as file:
        return individual_from_dict(json.load(file))


def save_checkpoint(population, generation, best_individual):
    """학습을 중간부터 이어가기 위한 checkpoint를 저장합니다."""
    ensure_storage_dirs()
    data = {
        "generation": generation,
        "population": [individual_to_dict(individual) for individual in population],
        "best": individual_to_dict(best_individual, generation),
    }
    with CHECKPOINT_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_checkpoint():
    """저장된 checkpoint를 불러옵니다."""
    if not CHECKPOINT_PATH.exists():
        return None
    with CHECKPOINT_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return {
        "generation": data["generation"],
        "population": [
            individual_from_dict(individual)
            for individual in data["population"]
        ],
        "best": individual_from_dict(data["best"]),
    }


def append_history(generation, population):
    """세대별 학습 기록을 CSV에 추가합니다."""
    ensure_storage_dirs()
    best = population[0]
    average_fitness = sum(
        individual.fitness for individual in population
    ) / len(population)
    is_new_file = not HISTORY_PATH.exists()

    with HISTORY_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if is_new_file:
            writer.writerow([
                "generation",
                "best_fitness",
                "best_score",
                "best_steps",
                "average_fitness",
            ])
        writer.writerow([
            generation,
            best.fitness,
            best.score,
            best.steps,
            round(average_fitness, 2),
        ])

