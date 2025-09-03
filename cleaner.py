import pandas as pd
import numpy as np
import stats


def clean(data):
    # df = pd.DataFrame()
    # remove 'ica_u_ml' abnormal data
    data['ica_u_ml'] = data.ica_u_ml.map(lambda x: x if x not in ['1:10', '10-Jan', '1:32', '28-05-2025 ', ' -', '>280'] else np.nan)
    data['ica_u_ml'] = data.ica_u_ml.map(lambda x: x if isinstance(x, float) else float(x.replace(',', '.')))
    data.loc[(data['creatinine_micromol_l'] > 1000) | (data['creatinine_micromol_l'] < 1), [
        'creatinine_micromol_l']] = np.nan
    # 'gfr_ckd_epi'
    data.loc[(data['gfr_ckd_epi'] > 500), ['gfr_ckd_epi']] = np.nan
    # 'c_peptide_levels_ng_ml'
    data.loc[(data['c_peptide_levels_ng_ml'] > 20), ['c_peptide_levels_ng_ml']] = np.nan
    return data


def clean_outliers(data):
    if len(data) > 5:
        data = data.dropna()
        # Calculate the 25th percentile.
        qOne = data.quantile(0.25)
        # Calculate the 75th percentile.
        qThree = data.quantile(0.75)
        iqr = stats.iqr(data)
        minimum = qOne - (1.5 * iqr)
        maximum = qThree + (1.5 * iqr)
        data = data[(data > minimum) & (data < maximum)]
    return data
