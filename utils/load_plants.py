
import pandas as pd

PLANTS_CSV = "data/plants.csv"
CARE_LOG_CSV = "data/care_log.csv"
DUE_LOG_CSV = "data/due_log.csv"

GROWTH_LOG_CSV = "data/growth_measurements.csv"
PHOTOS_CSV = "data/plant_photos.csv"
PROBLEM_RULES = "data/plant_problem_rules.csv"


plants_df = pd.read_csv(PLANTS_CSV)
care_log_df = pd.read_csv(CARE_LOG_CSV)
due_log_df = pd.read_csv(DUE_LOG_CSV)

growth_df = pd.read_csv(GROWTH_LOG_CSV)
photos_df = pd.read_csv(PHOTOS_CSV)
problem_df = pd.read_csv(PROBLEM_RULES)


def load_growth():
    return growth_df.copy()

def load_photos():
    return photos_df.copy()


def load_problem_rules():
    return problem_df.copy()


def load_problems():
    return problem_df.copy()



def load_plants():
    return plants_df.copy()


def load_care_log():
    return care_log_df.copy()


def load_due_log():
    global due_log_df
    due_log_df = pd.read_csv(DUE_LOG_CSV)
    return due_log_df.copy()


def save_plants():
    plants_df.to_csv(PLANTS_CSV, index=False)


def save_care_log():
    care_log_df.to_csv(CARE_LOG_CSV, index=False)


def save_due_log(df):
    global due_log_df
    due_log_df = df.copy()
    df.to_csv(DUE_LOG_CSV, index=False)

def save_growth(df):
    global growth_df
    growth_df = df.copy()
    df.to_csv(GROWTH_LOG_CSV, index=False)


def save_photos(df):
    global photos_df
    photos_df = df.copy()
    df.to_csv(PHOTOS_CSV, index=False)


def save_problem(df):
    global problem_df
    problem_df = df.copy()
    df.to_csv(PROBLEM_RULES, index=False)



