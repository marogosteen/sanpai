import os


class WriteLogService:
    path = "log/"

    def __init__(self) -> None:
        pass

    def make_log_directory(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def write_log(self, dna_group, score_list, ranking):
        num = 1
        path = self.path+f"{num}.txt"
        while os.path.exists(path):
            num += 1
            path = self.path+f"{num}.txt"

        with open(path, "w") as f:
            for index, dna_i in enumerate(ranking):
                line = f"{index+1}: ".ljust(5)
                line += f"{round(score_list[dna_i], 3)} km".ljust(13)
                line += ",".join(list(map(str, dna_group[dna_i])))
                line += "\n"
                f.write(line)
