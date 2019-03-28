import csv
from statistics import mean, median
from settings import STARTTIME, HEADER1, HEADER2


def isfloat(value):
    """ returns true if value can be a float """
    try:
        float(value)
        return True
    except ValueError:
        return False


def column(matrix, i):
    """ returns the column of index i removing headers """
    return [row[i] for row in matrix if isfloat(row[i])]


def print_info(c, timestamp):
    """ print creature info on console """
    print(f"\n[{timestamp}] [{id(c)}] [Fitness: {c.fitness()}] Age: {c.age} seconds." +
          f" F.Eaten: {c.eaten}\n" +
          f"currHP: {c.health}, Gen: {c.gen}, Childs: {c.childs}\n" +
          f"DNA: {c.dna}\n" +
          f"FoodAttr: {c.food_attraction}, PoisonAttr: {c.poison_attraction}\n" +
          f"FoodDist: {c.food_dist}, PoisonDist: {c.poison_dist}\n" +
          f"MaxHealth: {c.max_health}, MaxVel: {c.max_vel}, Size: {c.size}\n" +
          f"MaxSteer: {c.max_steer_force}, DirAngleMult: {c.dir_angle_mult}\n")


class Datastats:
    """ stores statistics, history and other data from the game """

    def __init__(self):
        self.fittest = None
        self.current_fittest = None
        self.oldest = None
        self.fitness_record = 0
        self.age_record = 0

        self.temp_history = []
        self.history = []
        self.temp_stats_history = []
        self.stats_history = []
        self.last_save = 0
        self.header_saved = [False, False]

        self.csv_name1 = STARTTIME + "_history.csv"
        self.csv_name2 = STARTTIME + "_stats.csv"

        # 0: fitness,   1: age,        2: f.eaten, 3: MaxVel_MaxHP
        # 4: FAttr,     5: PAttr,      6: FDist,   7: PDist
        # 8: MaxSteerF, 9: DirAngMult
        self.means = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.medians = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def save_csv(self):
        with open(self.csv_name1, mode='a', newline='') as data_file:
            data_writer = csv.writer(
                data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # check if we saved the header (not saved = new file)
            if not self.header_saved[0]:
                data_writer.writerow(HEADER1)
                self.header_saved[0] = True
            for line in self.temp_history:
                data_writer.writerow(line)
        self.temp_history.clear()
        with open(self.csv_name2, mode='a', newline='') as data_file:
            data_writer = csv.writer(
                data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # check if we saved the header (not saved = new file)
            if not self.header_saved[1]:
                data_writer.writerow(HEADER2)
                self.header_saved[1] = True
            for line in self.temp_stats_history:
                data_writer.writerow(line)
        self.temp_stats_history.clear()

    def calc_stats(self, timestamp):
        if self.history:
            row = []
            row.append(timestamp)
            for i in range(len(self.means)):
                self.means[i] = mean(column(self.history, i+1))
                self.medians[i] = median(column(self.history, i+1))
                row.append(self.means[i])
                row.append(self.medians[i])

            self.temp_stats_history.append(row)
            self.stats_history.append(row)

        print("~~~~~~~~~~")
        print(f"Mean Fitness:\t{self.means[0]}")
        print(f"Median Fitness:\t{self.medians[0]}")
        print("~~~~~~~~~~")

    def print_stats(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for i in range(len(self.means)):
            if i == 0:
                continue
            print(f"Mean {HEADER1[i]}:\t{self.means[i-1]}")
            print(f"Median {HEADER1[i]}:\t{self.medians[i-1]}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")