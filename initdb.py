import sqlite3
import config
import pandas as pd


if __name__ == "__main__":
    conn = sqlite3.connect(config.DATABASE_FILEPATH())
