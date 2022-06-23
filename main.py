import time

import temple
from ga import Ga

DATASET_PATH = "data/Location33.DAT"
MUTATION_NUM = 20
INVERSUS_NUM = 20
TRANSLOCATION_NUM = 20
CROSS_NUM = 20
ELITE_NUM = 25
GENERATION = 8192

# 交差は２個体が必要．child_coundが奇数だとStopIterationErrorが生じる．
if CROSS_NUM % 2 != 0:
    # TODO write error message
    raise ValueError("")

temple_group = []
with open(DATASET_PATH) as f:
    for line in f.readlines():
        line = line.strip().split()
        temple_group.append(
            temple.Temple(
                int(line[0]),
                line[1],
                latitude=float(line[2]),
                longitude=float(line[3])))

temple_group = temple.TempleGroup(
    temple_group, start_id=33, goal_id=33)
ga = Ga(temple_group)

start_time = time.time()
score_list = ga.scores(ga.dna_group)
before_score = min(score_list)
for gene in range(GENERATION):
    elite_dnas = ga.elite_dnas(score_list, ELITE_NUM)

    ga.mutation(ga.tournament(score_list, MUTATION_NUM))
    ga.inversus(ga.tournament(score_list, INVERSUS_NUM))
    ga.translocation(ga.tournament(score_list, TRANSLOCATION_NUM))
    ga.cross(ga.tournament(score_list, CROSS_NUM))

    ga.replace_elite_dnas(elite_dnas)
    score_list = ga.scores(ga.dna_group)
    best_score = min(score_list)

    if best_score > before_score:
        print(
            "error",
            f"before_score: {before_score}",
            f"best_score: {best_score}",
            sep="\n")

    if gene % 200 == 0:
        print(f"{gene} min: ", round(best_score, 3), "km")
    before_score = best_score

score_list = ga.scores(ga.dna_group, selection=True)
ranking = sorted(range(len(score_list)), key=score_list.__getitem__)
for i, dna_i in enumerate(ranking):
    print(f"{i}: {dna_i}".ljust(10), ga.dna_group[dna_i], round(score_list[dna_i], 3))

most_elite = ga.dna_group[score_list.index(best_score)]
print(
    f"\n{gene+1} min: {round(best_score, 3)} km",
    f"most elitte: {most_elite}",
    f"sec: {round(time.time() - start_time, 1)}",
    f"elite num: {ELITE_NUM}",
    sep="\n",
    end="\n\n")
