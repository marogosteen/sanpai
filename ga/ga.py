import math
import random
import string

import temple

from ga import algo


MUTATE_INDEX_COUNT = 2
INVERSUS_INDEX_COUNT = 2
TRANS_INDEX_COUNT = 2
CROSS_INDEX_COUNT = 2
NOT_MATCH = 4
S = string.digits+string.ascii_lowercase


def match_count(dna1: list[int], dna2: list[int]) -> int:
    return [e1 == e2 for e1, e2 in zip(dna1, dna2)].count(True)


class Ga:
    @property
    def dna_size(self) -> int:
        return self.__dna_size

    @property
    def group_size(self) -> int:
        return self.__group_size

    def __init__(self, temple_group: temple.TempleGroup) -> None:
        self.__temple_gourp = temple_group
        temple_count = len(temple_group)
        self.__group_size = int(
            temple_count * math.log(temple_count-1) / math.log(2))

        # the start point and goal point are fixed. therefore, it is not included in the DNA.
        self.__dna_size = temple_count - 1
        self.dna_group: list[list] = []
        for _ in range(self.__group_size):
            dna = list(range(1, temple_count))
            random.shuffle(dna)
            self.dna_group.append(dna)

    def scores(self, dna_list: list[list], selection: bool = True) -> list[float]:
        score_list = []
        for dna in dna_list:
            score = 0
            score += self.__temple_gourp.distance(
                self.__temple_gourp.start_id, dna[0])
            score += self.__temple_gourp.distance(
                dna[-1], self.__temple_gourp.goal_id)

            for dna_index in range(len(dna)-1):
                start_id = dna[dna_index]
                goal_id = dna[dna_index+1]
                score += self.__temple_gourp.distance(start_id, goal_id)
            score_list.append(score)

        # 最終結果の表示などは淘汰圧を必要としない．
        if not selection:
            return score_list

        return self.selection(score_list)

    def selection(self, score_list: list[float]) -> list[float]:
        max_score = max(score_list)
        reverse_ranking = sorted(
            range(len(score_list)), key=score_list.__getitem__, reverse=True)
        for i in range(1, len(reverse_ranking)):
            dna_index = reverse_ranking[i-1]
            dna = self.dna_group[dna_index]
            good_dna_index = reverse_ranking[i]
            good_dna = self.dna_group[good_dna_index]
            if max(match_count(dna[-1::-1], good_dna), match_count(dna, good_dna)) >= self.dna_size - NOT_MATCH:
                score_list[dna_index] = max_score
        return score_list

    def elite_dnas(self, score_list: list[float], elite_count: int) -> list[list]:
        if elite_count > self.group_size:
            raise ValueError(
                "the value of elite_count is greater than gropu_size.")

        elite_dnas = []
        ranking = sorted(range(len(score_list)), key=score_list.__getitem__)
        for dna_index in ranking[:elite_count]:
            dna = self.dna_group[dna_index]
            elite_dnas.append(dna.copy())

        return elite_dnas

    def replace_dnas(self, elite_dnas: list[list]) -> None:
        # 新しくscore計算した方が多様性の担保できる
        score_list = self.scores(self.dna_group)
        reverse_ranking = sorted(
            range(len(score_list)), key=score_list.__getitem__)[-1::-1]

        for dna_index, elite in zip(reverse_ranking, elite_dnas):
            self.dna_group[dna_index] = elite

    def tournament(self, score_list: list[float], select_size: int, tournament_size: int = 2) -> list[int]:
        if select_size > self.__group_size//2:
            raise ValueError(
                "the value of select is greater than group_size.")

        selected_dnas = []
        while select_size > len(selected_dnas):
            min_score = max(score_list)
            min_index = score_list.index(min_score)

            for random_index in random.sample(range(self.__group_size), k=tournament_size):
                score = score_list[random_index]
                if min_score >= score:
                    min_score = score
                    min_index = random_index

            if not min_index in selected_dnas:
                selected_dnas.append(min_index)

        return selected_dnas

    def mutation(self, dna_indices: list) -> list:
        mutated_dnas = []
        for dna_index in dna_indices:
            selected_dna = self.dna_group[dna_index].copy()
            mutate_indices = random.sample(
                range(self.dna_size), k=MUTATE_INDEX_COUNT)
            mutated_dnas.append(algo.mutation(
                selected_dna, mutate_indices)
            )
        return mutated_dnas

    def inversus(self, dna_indices: list) -> list:
        mutated_dnas = []
        for dna_index in dna_indices:
            selected_dna = self.dna_group[dna_index].copy()
            inversus_indices = random.sample(
                range(self.dna_size+1), k=INVERSUS_INDEX_COUNT)
            mutated_dnas.append(algo.inversus(
                selected_dna, inversus_indices)
            )
        return mutated_dnas

    def translocation(self, dna_indices: list) -> list:
        mutated_dnas = []
        for dna_index in dna_indices:
            selected_dna = self.dna_group[dna_index]
            start, end = sorted(random.sample(
                range(self.dna_size+1), k=TRANS_INDEX_COUNT))
            mutated_dnas.append(
                algo.translocation(selected_dna, start, end)
            )
        return mutated_dnas

    def cross(self, dna_indices: list) -> list:
        mutated_dnas = []
        while len(dna_indices) > 0:
            dna_index1 = dna_indices.pop(0)
            dna_index2 = dna_indices.pop(0)
            parent1 = self.dna_group[dna_index1].copy()
            parent2 = self.dna_group[dna_index2].copy()
            start, end = sorted(
                random.sample(range(self.dna_size), k=CROSS_INDEX_COUNT))
            mutated_dnas.extend(algo.cross(parent1, parent2, start, end))
            return mutated_dnas

    def __dna_to_string(self, dna: list[int]) -> string:
        result = ""
        for i in dna:
            result += S[i]
        return result

    def __string_to_dna(self, strings: str) -> list[int]:
        dna = []
        for s in strings:
            dna.append(S.index(s))

    def show_ranking(self):
        score_list = self.scores(self.dna_group, selection=False)
        ranking = sorted(range(len(score_list)), key=score_list.__getitem__)
        for i, dna_i in enumerate(ranking):
            print(
                f"{i}: {dna_i}".ljust(8),
                f"{round(score_list[dna_i], 3)} km".ljust(13),
                self.dna_group[dna_i])
