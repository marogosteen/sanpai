from functools import lru_cache
import random


def multi_pop(obj: list, start: int, end: int) -> list:
    for i in sorted(range(start, end), reverse=True):
        obj.pop(i)
    return obj


def mutation(selected_dna: list, mutate_indices: list) -> list[int]:
    tmp_dna = selected_dna.copy()
    selected_dna[mutate_indices[0]] = tmp_dna[mutate_indices[1]]
    selected_dna[mutate_indices[1]] = tmp_dna[mutate_indices[0]]
    return selected_dna


def inversus(selected_dna: list, inversus_indices: list) -> list[int]:
    start = min(inversus_indices)
    end = max(inversus_indices)
    selected_dna[start:end] = selected_dna[start:end][-1::-1]
    if inversus_indices[0] > inversus_indices[1]:
        selected_dna.reverse()
    return selected_dna


def translocation(selected_dna: list, start: int, end: int) -> list[int]:
    part_dna = selected_dna[start:end]
    selected_dna = multi_pop(selected_dna, start, end)
    insert_index = random.randint(0, len(selected_dna))
    selected_dna[insert_index:insert_index] = part_dna
    return selected_dna


def cross(parent1: list, parent2: list, start: int, end: int) -> list[list]:
    part1 = parent1[start:end]
    part2 = parent2[start:end]
    popped_dna1 = multi_pop(parent1, start, end)
    popped_dna2 = multi_pop(parent2, start, end)

    dup_indices1 = []
    dup_indices2 = []
    for v1, v2 in zip(part1, part2):
        if v2 in popped_dna1:
            dup_indices1.append(popped_dna1.index(v2))
        if v1 in popped_dna2:
            dup_indices2.append(popped_dna2.index(v1))

    child1 = popped_dna1.copy()
    child2 = popped_dna2.copy()
    for i1, i2 in zip(dup_indices1, dup_indices2):
        child1[i1] = popped_dna2[i2]
        child2[i2] = popped_dna1[i1]

    child1[start:start] = part2
    child2[start:start] = part1

    return [child1, child2]


@lru_cache(maxsize=4096)
def levenshtein(s, t):
    if not s:
        return len(t)
    if not t:
        return len(s)
    if s[0] == t[0]:
        return levenshtein(s[1:], t[1:])
    l1 = levenshtein(s, t[1:])
    l2 = levenshtein(s[1:], t)
    l3 = levenshtein(s[1:], t[1:])
    return 1 + min(l1, l2, l3)
