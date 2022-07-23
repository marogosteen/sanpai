import random
import time

import temple
from ga import Ga
from services import WriteLogService

DATASET_PATH = "data/Location33.DAT"
MUTATION_NUM = 70
INVERSUS_NUM = 70
TRANSLOCATION_NUM = 70
CROSS_NUM = 70
ELITE_NUM = 20
STOP_TRIGGER = 2000
GROUP_SIZE = 500

service = WriteLogService()
service.make_log_directory()

# 交差は２個体が必要．child_coundが奇数だとStopIterationErrorが生じる．
if CROSS_NUM % 2 != 0:
    # TODO write error message
    raise ValueError("")

temple_group = []
with open(DATASET_PATH, encoding="utf-8") as f:
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
ga = Ga(temple_group, GROUP_SIZE)

start_time = time.time()
score_list = ga.scores(ga.dna_group)
before_score = min(score_list)
counter = 0
while True:
    counter += 1
    if counter == STOP_TRIGGER:
        break

    elite_dnas = ga.elite_dnas(score_list, ELITE_NUM)

    mutated_dnas = []
    mutated_dnas.extend(ga.mutation(ga.tournament(score_list, MUTATION_NUM)))
    mutated_dnas.extend(ga.inversus(ga.tournament(score_list, INVERSUS_NUM)))
    mutated_dnas.extend(ga.translocation(
        ga.tournament(score_list, TRANSLOCATION_NUM)))
    mutated_dnas.extend(ga.cross(ga.tournament(score_list, CROSS_NUM)))

    ga.replace_dnas(mutated_dnas)
    ga.replace_dnas(elite_dnas)
    score_list = ga.scores(ga.dna_group)
    after_score = min(score_list)

    if round(after_score, 3) == 803.26:
        print(f"{counter} min: ", round(after_score, 3), "km")
        break

    if counter % 200 == 0:
        ranking = sorted(range(len(score_list)), key=score_list.__getitem__)
        for dna_index in ranking[int(ga.group_size*0.4):]:
            ga.dna_group[dna_index] = ga.new_dna()
        print(f"{counter} min: ", round(after_score, 3), "km")

    if before_score > after_score:
        counter = 0

    before_score = after_score

print("\nDone\n")

scores = ga.scores(ga.dna_group, selection=False)
ranking = sorted(range(len(scores)), key=scores.__getitem__)
service.write_log(ga.dna_group, scores, ranking)

print(
    f"\nsec: {round(time.time() - start_time, 1)}",
    f"elite num: {ELITE_NUM}",
    sep="\n",
    end="\n\n")
