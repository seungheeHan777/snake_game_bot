"""유전 알고리즘 학습 루프입니다."""

from random import choices, random, sample, uniform

from ga_bot.policy import (
    FEATURE_NAMES,
    SAMPLE_WEIGHT_PRESETS,
    Individual,
    ensure_weight_size,
)
from ga_bot.simulation import simulate_game
from ga_bot.storage import (
    append_history,
    load_checkpoint,
    save_best_model,
    save_checkpoint,
    save_score400_candidate,
)
from snake_core import BOARD_CELLS

POPULATION_SIZE = 40
GENERATIONS = 100
MUTATION_RATE = 0.18
MUTATION_AMOUNT = 0.35
ELITE_COUNT = 4
INITIAL_NOISE_SCALE = 0.35
EARLY_STOP_PATIENCE = 50


def create_individual(preset_name="balanced_v1"):
    """preset 기반 가중치에 작은 노이즈를 더해 개체를 만듭니다."""
    base_weights = SAMPLE_WEIGHT_PRESETS.get(
        preset_name,
        SAMPLE_WEIGHT_PRESETS["balanced_v1"],
    )
    weights = []
    for base_weight in ensure_weight_size(base_weights):
        weights.append(base_weight + uniform(-INITIAL_NOISE_SCALE, INITIAL_NOISE_SCALE))
    return Individual(weights)


def create_population(preset_name="balanced_v1"):
    """초기 세대를 만듭니다."""
    return [create_individual(preset_name=preset_name) for _ in range(POPULATION_SIZE)]


def evaluate_population(population):
    """세대 전체를 평가합니다."""
    for individual in population:
        simulate_game(individual)
    population.sort(key=individual_rank, reverse=True)


def individual_rank(individual):
    """score를 최우선으로 보고 fitness를 보조 기준으로 사용합니다."""
    return individual.score, individual.fitness


def select_parent(population):
    """fitness가 높은 개체가 더 자주 뽑히는 방식으로 부모를 선택합니다."""
    total_fitness = sum(individual.fitness for individual in population)
    if total_fitness <= 0:
        return sample(population, 1)[0]
    return choices(
        population,
        weights=[individual.fitness for individual in population],
        k=1,
    )[0]


def crossover(parent_a, parent_b):
    """두 부모의 가중치를 섞어서 자식을 만듭니다."""
    weights = []
    for index in range(len(FEATURE_NAMES)):
        if random() < 0.5:
            weights.append(parent_a.weights[index])
        else:
            weights.append(parent_b.weights[index])
    return Individual(weights)


def mutate(individual):
    """일정 확률로 가중치를 조금 변경합니다."""
    for index in range(len(individual.weights)):
        if random() < MUTATION_RATE:
            individual.weights[index] += uniform(-MUTATION_AMOUNT, MUTATION_AMOUNT)


def next_generation(population):
    """엘리트 보존, 선택, 교차, 변이로 다음 세대를 만듭니다."""
    next_population = [
        Individual(individual.weights.copy())
        for individual in population[:ELITE_COUNT]
    ]

    while len(next_population) < POPULATION_SIZE:
        parent_a = select_parent(population)
        parent_b = select_parent(population)
        child = crossover(parent_a, parent_b)
        mutate(child)
        next_population.append(child)

    return next_population


def train(generations=GENERATIONS, resume=True, early_stop_patience=EARLY_STOP_PATIENCE):
    """여러 세대를 학습하고 가장 좋은 개체를 반환합니다."""
    checkpoint = load_checkpoint() if resume else None
    if checkpoint:
        population = checkpoint["population"]
        start_generation = checkpoint["generation"] + 1
        best_individual = checkpoint["best"]
    else:
        population = create_population()
        start_generation = 1
        best_individual = None

    end_generation = start_generation + generations - 1
    no_improve_generations = 0
    for generation in range(start_generation, end_generation + 1):
        evaluate_population(population)

        for rank, individual in enumerate(population, start=1):
            if individual.score >= BOARD_CELLS:
                save_score400_candidate(individual, generation, rank)

        improved = False
        if (
            best_individual is None
            or individual_rank(population[0]) > individual_rank(best_individual)
        ):
            best_individual = population[0]
            save_best_model(best_individual, generation)
            improved = True

        append_history(generation, population)
        save_checkpoint(population, generation, best_individual)
        print(
            f"generation={generation} "
            f"fitness={population[0].fitness} "
            f"score={population[0].score} "
            f"steps={population[0].steps}"
        )

        if improved:
            no_improve_generations = 0
        else:
            no_improve_generations += 1

        if (
            early_stop_patience is not None
            and early_stop_patience > 0
            and no_improve_generations >= early_stop_patience
        ):
            print(
                f"early-stop: no best improvement for "
                f"{no_improve_generations} generations"
            )
            break

        population = next_generation(population)

    return best_individual
