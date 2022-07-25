import time

import temple
from ga import Ga
from services import WriteLogService

DATASET_PATH = "data/Location33.DAT"
MUTATION_NUM = 20
INVERSUS_NUM = 20
TRANSLOCATION_NUM = 20
CROSS_NUM = 20
ELITE_NUM = 10
STOP_TRIGGER = 3000
GROUP_SIZE = 1000
CLUSTER = 10

is_exit = False

def hoge(ga: Ga):
    score_list = ga.scores(ga.dna_group)
    before_score = min(score_list)
    counter = 0
    no_progress = 0
    while True:
        counter += 1
        no_progress += 1
        if no_progress == STOP_TRIGGER:
            break

        elite_dnas = ga.elite_dnas(score_list, ELITE_NUM)

        mutated_dnas = []
        mutated_dnas.extend(ga.mutation(ga.tournament(score_list, MUTATION_NUM)))
        mutated_dnas.extend(ga.inversus(ga.tournament(score_list, INVERSUS_NUM)))
        mutated_dnas.extend(ga.translocation(
            ga.tournament(score_list, TRANSLOCATION_NUM)))
        mutated_dnas.extend(ga.cross(ga.tournament(score_list, CROSS_NUM)))

        ga.replace_dnas(mutated_dnas)
        if counter % 1000 == 0:
            # ranking = sorted(range(len(score_list)), key=score_list.__getitem__)
            # for dna_index in ranking[int(ga.group_size*0.1):]:
            for dna_index in range(ga.group_size):
                ga.dna_group[dna_index] = ga.new_dna()
            counter = 0
            print("reloaded DNAs")

        ga.replace_dnas(elite_dnas)
        score_list = ga.scores(ga.dna_group)
        after_score = min(score_list)

        if round(after_score, 3) == 803.26:
            print(f"{no_progress} min: ", round(after_score, 3), "km")
            return True

        if no_progress % 200 == 0:
            print(f"{no_progress} min: ", round(after_score, 3), "km")

        if before_score > after_score:
            no_progress = 0

        before_score = after_score

if not GROUP_SIZE % CLUSTER == 0:
    raise ValueError

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
mother_ga = Ga(temple_group, GROUP_SIZE)

start_time = time.time()

dna_index = 0
for cluster_num in range(CLUSTER):
    print("\ncluster:", cluster_num)
    ga = Ga(temple_group, GROUP_SIZE//CLUSTER)
    if is_exit:
        break

    if hoge(ga):
        is_exit = True

    for dna in ga.dna_group:
        mother_ga.dna_group[dna_index] = dna
        dna_index += 1

print("mother ga")
ga = mother_ga
hoge(ga)

print("\nDone\n")

scores = ga.scores(ga.dna_group, selection=False)
ranking = sorted(range(len(scores)), key=scores.__getitem__)
service.write_log(ga.dna_group, scores, ranking)

print(
    f"\nsec: {round(time.time() - start_time, 1)}",
    f"elite num: {ELITE_NUM}",
    sep="\n",
    end="\n\n")
