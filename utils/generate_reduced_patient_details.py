import itertools

import numpy as np
import pandas as pd


def is_healthy_volunteer(x, group_details):
    if "SKIN" in x.name or (
        x.name in group_details.index.values.tolist()
        and group_details.loc[x.name] == "Healthy volunteer"
    ):
        return True
    elif "Study_" in x.index:
        return False
    else:
        return False


def main():
    # 1. ITA_raw.parquet: can be kept as is.
    df_ita = pd.read_parquet("patient_details/ITA_raw.parquet")
    print(df_ita.head())
    df_ita.to_parquet("reduced_patient_details/ITA_raw.parquet")

    # 2. MITOX_characteristics.csv
    df_mitox_characteristics = pd.read_csv(
        "patient_details/MITOX_characteristics.csv", index_col=0
    )
    print(df_mitox_characteristics.head())

    bins = range(0, 101, 20)

    labels = [f"{lo}-{hi - 1}" for lo, hi in itertools.pairwise(bins)]

    df_mitox_characteristics["Age"] = pd.cut(
        df_mitox_characteristics["Age"], bins=bins, labels=labels, right=False
    )

    # Bin BMI
    bins = [0, 18.5, 25, 30, 35, 40]

    labels = [f"{lo}-{hi - 1}" for lo, hi in itertools.pairwise(bins)]

    df_mitox_characteristics["BMI"] = pd.cut(
        df_mitox_characteristics["BMI"], bins=bins, labels=labels, right=False
    )
    print(df_mitox_characteristics.head())
    df_mitox_characteristics.to_csv("reduced_patient_details/MITOX_characteristics.csv")

    # 3. MITOXGroups.xlsx
    df_mitox_groups = pd.read_excel("patient_details/MITOXGroups.xlsx", index_col=0)
    print(df_mitox_groups)

    # MITOXPAISKINTONEAgeSex
    df_mitox_age_sex = pd.read_csv(
        "patient_details/MITOXPAISKINTONEAgeSex.csv", index_col=0
    )
    df_mitox_age_sex["Group"] = df_mitox_age_sex.apply(
        lambda x: (
            "Healthy volunteer"
            if is_healthy_volunteer(x, df_mitox_groups["Group"])
            else "Affected patient"
        ),
        axis=1,
    )

    bins = range(0, 101, 20)

    labels = [f"{lo}-{hi - 1}" for lo, hi in itertools.pairwise(bins)]

    df_mitox_age_sex["Age"] = pd.cut(
        df_mitox_age_sex["Age"], bins=bins, labels=labels, right=False
    )

    print(df_mitox_age_sex)


if __name__ == "__main__":
    main()
