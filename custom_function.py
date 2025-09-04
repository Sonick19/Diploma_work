import matplotlib.pyplot as plt
from cleaner import clean_outliers
from scipy import stats
import scikit_posthocs as sp


def continuous_data_vis(clean=False, comment=''):
    def inner(dataset, column, path='',):
        plt.figure()
        dt = dataset[column].dropna()
        if clean:
            dt = clean_outliers(dt)
        plt.hist(dt, density=False, bins=100)
        plt.axvline(dt.median(), color="black", ls="--", label="Median")
        plt.title(column)
        plt.legend()
        plt.savefig(f'{path}/image/contin_vis_{column}{comment}.png')
        plt.close()
        return {"image": f'image/contin_vis_{column}{comment}.png', "title": f'{comment}'}
    return inner


def continuous_compare_vis(search_column=None, clean=False, comment=''):
    def inner(dataset, column, path=''):
        plt.figure()
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
        plt.xticks(rotation=10)
        plt.title(column)
        plt.savefig(f'{path}/image/contin_compare_{column}{comment}.png')
        plt.close()
        return {"image": f'image/contin_compare_{column}{comment}.png', "title": f'{comment}'}
    return inner


def kruskal_test(search_column=None, clean=False, comment=''):
    def inner(dataset, column, path=''):
        data_list = []
        label_list = []
        for key, elem in search_column.items():
            for category in elem:
                data = dataset[dataset[key] == category][column].dropna()
                if clean:
                    data = clean_outliers(data)
                data_list.append(data.values)
                label_list.append(f'{key}_{category}')
        result = stats.kruskal(*data_list)
        value = result[1]
        try:
            res = sp.posthoc_dunn(data_list, p_adjust="holm")
            # Apply styling
            res = res.style.map(__highlight_significant).to_html()
        except:
            res = ''

        if value < 0.05:
            return {"title": f'Kruskal-Wallis H-test {comment} - <span style="color:red;">Significant</span>',
                    "text": f'p-value = {value}\n{res}'}
        else:
            return {"title": f'Kruskal-Wallis H-test {comment} - NONsignificant',
                    "text": f'p-value = {value}'}
    return inner


def __highlight_significant(val):
    color = 'red' if val < 0.05 else 'black'
    return f'color: {color}'


