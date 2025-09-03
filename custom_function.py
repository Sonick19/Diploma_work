import matplotlib.pyplot as plt
from cleaner import clean_outliers

def continuous_data_vis(dataset, column, path='', clean=False, search_column=None, comment=''):
    plt.figure()
    dt = dataset[column].dropna()
    plt.hist(dt, density=False, bins=100)
    plt.axvline(dt.median(), color="black", ls="--", label="Median")
    plt.title(column)
    plt.legend()
    plt.savefig(f'{path}/contin_vis_{column}{comment}.png')
    plt.close()
    return {"image": f'contin_vis_{column}{comment}.png', "title": f'{comment}'}


def continuous_compare_vis(dataset, column, path='', clean=False, search_column=None, comment=''):
    plt.figure()
    # if column in ['height_cm', 'weight_kg', 'bmi', 'waist_circumference_cm', 'hip_circumference_cm',]:
    #     counting_c_w = data[(data['casecontrol'] == 2) & (data['patientsex'] == 1)][column].dropna()
    #     counting_c_m = data[(data['casecontrol'] == 2) & (data['patientsex'] == 2)][column].dropna()
    #     counting_t_w = data[(data['casecontrol'] == 1) & (data['patientsex'] == 1)][column].dropna()
    #     counting_t_m = data[(data['casecontrol'] == 1) & (data['patientsex'] == 2)][column].dropna()
    #     plt.boxplot([counting_c_w, counting_c_m, counting_t_w, counting_t_m],
    #                 labels=["control_woman", "control_man", "test_woman", "test_man"])
    if True:
        data_list = []
        label_list = []
        for key, elem in search_column.items():
            for category in elem:
                data = dataset[dataset[key] == category][column].dropna()
                if clean:
                    data = clean_outliers(data)
                data_list.append(data)
                label_list.append(f'{key}_{category}\n{len(data)}')
        plt.boxplot(data_list, labels=label_list)
    plt.title(column)
    plt.savefig(f'{path}/contin_compare_{column}{comment}.png')
    plt.close()
    return {"image": f'contin_compare_{column}{comment}.png', "title": f'{comment}'}