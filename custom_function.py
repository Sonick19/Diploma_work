import matplotlib.pyplot as plt
from cleaner import clean_outliers
from scipy import stats
import scikit_posthocs as sp
import pandas as pd
import numpy as np
import simple_icd_10 as icd


def continuous_data_vis(clean=False, comment=''):
    def inner(dataset, column, path='',):
        plt.figure()
        dt = dataset.data[column].dropna()
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
        data_list, label_list = __split_by_group(dataset.data, column, search_column, clean)
        for i in range(len(label_list)):
            label_list[i] = label_list[i] + f'\n{len(data_list[i])}'
        plt.boxplot(data_list, labels=label_list)
        plt.xticks(rotation=10)
        plt.title(column)
        plt.savefig(f'{path}/image/contin_compare_{column}{comment}.png')
        plt.close()
        return {"image": f'image/contin_compare_{column}{comment}.png', "title": f'{comment}'}
    return inner


def kruskal_test(search_column=None, clean=False, comment=''):
    def inner(dataset, column, path='', check=False):
        data_list, label_list = __split_by_group(dataset.data, column, search_column, clean)
        result = stats.kruskal(*data_list)
        value = result[1]
        if value < 0.05:
            if check:
                return True
            try:
                res = sp.posthoc_dunn(data_list, p_adjust="holm")
                # Apply styling
                res = res.style.map(__highlight_significant).to_html()
            except:
                res = ''
            return {"title": f'Kruskal-Wallis H-test {comment} - <span style="color:red;">Significant</span>',
                    "text": f'p-value = {value}\n{res}'}
        else:
            if check:
                return False
            return {"title": f'Kruskal-Wallis H-test {comment} - NONsignificant',
                    "text": f'p-value = {value}'}
    return inner


def categorical_compare_tc_vis(search_column=None,  comment=''):
    def inner(dataset, column, path=''):
        # specify possible categories in column
        index = dataset.data[column].value_counts().index
        data_list, label_list = __split_by_group(dataset.data, column, search_column, method=pd.Series.value_counts, method_arg={})
        translation = column in dataset.keyword
        result = viz(column, data_list, label_list, index, translation, dataset.keyword.get(column),
                     path, comment)
        return result
    return inner


def chi_test(search_column=None, comment=''):
    def inner(dataset, column, path='', check=False):
        reshape = pd.crosstab(dataset.data[column], dataset.data[str(*search_column.keys())])
        value = stats.chi2_contingency(reshape).pvalue
        if value < 0.05:
            if check:
                return True
            return {"title": f'Chi2-test {comment} - <span style="color:red;">Significant</span>',
                    "text": f'p-value = {value}'}
        else:
            if check:
                return False
            return {"title": f'Chi2-test {comment} - NONsignificant',
                    "text": f'p-value = {value}'}
    return inner

def categorical_multicolumn_test(search_column=None, comment='', mod = False):
    def inner(dataset, column, path=''):
        data_list, label_list = gen_multicolumn_lists(dataset, column, search_column)
        if mod:
            data_list = [icd_splitter(i) for i in data_list]
        # generate list of possible index
        index = [i.index.to_list() for i in data_list]
        index = [elem for i in index for elem in i]
        res_index = []
        # remove minor index and duplicates
        for elem in index:
            if elem not in res_index:
                counter = 0
                for record in data_list:
                    counter += record.get(elem, 0)
                if counter > len(data_list)*3:
                    res_index.append(elem)
        res_index.remove(np.nan)
        res_index.insert(0, np.nan)
        # generate graph
        result = viz(column, data_list, label_list, res_index,
                     path=path)
        return result
    return inner


def categorical_multicolumn_chi_test(search_column=None, comment='', mod=False, hide=False):
    def inner(dataset, column, path=''):
        result = ''
        data_list, label_list = gen_multicolumn_lists(dataset, column, search_column)
        if mod:
            data_list = [icd_splitter(i) for i in data_list]

        frame = {label_list[i]: data_list[i] for i in range(len(data_list))}
        data = pd.DataFrame(frame)
        data = data.fillna(0)
        for elem in data.index.to_list():
            if hide:
                save = False
            else:
                save = True
            d = {}
            for i in label_list:
                row_value = []
                for g in label_list:
                    sample = data.loc[[elem, np.nan], [i, g]]
                    res = stats.fisher_exact(sample).pvalue
                    row_value.append(res)
                    if hide:
                        if res < 0.05:
                            save = True
                d[i] = row_value
            if not save:
                continue
            res_data = pd.DataFrame(d, index=label_list)
            res = res_data.style.map(__highlight_significant).to_html()
            result += f'<h3>{elem}</h3>\n {res}\n'

        return {"title": f'Fisher-test {comment}',
                    "text": f'{result}'}

    return inner


def __highlight_significant(val):
    color = 'red' if val < 0.05 else 'black'
    return f'color: {color}'


def __split_by_group(dataset, column, search_column, clean=False, method=None, method_arg=None, drop=True):
    data_list = []
    label_list = []
    for key, elem in search_column.items():
        for category in elem:
            if drop:
                data = dataset[dataset[key] == category][column].dropna()
            else:
                data = dataset[dataset[key] == category][column]
            if clean:
                data = clean_outliers(data)
            if method:
                data = method(data, **method_arg)
            data_list.append(data)
            label_list.append(f'{key}_{category}')
    return data_list, label_list


def viz(column, data, label, index, translation=False, key_word=None, path='', comment='', size=(12.8, 9.6)):
    plt.figure(figsize=size)
    bottom = np.zeros(len(data))
    div = [i.sum() if i.sum() != 0 else 1 for i in data]
    for elem in index:
        label_info = [i.get(elem, default=0) for i in data]
        value = [round(label_info[i]/div[i], 3) for i in range(len(label_info))]
        if translation:
            elem = key_word[str(int(elem))]
        p = plt.bar(label, value,
                    label=f'{elem} {[f"{label[i][-1]}:{label_info[i]}" for i in range(len(label_info))]}',
                    bottom=bottom)
        bottom += value
        plt.bar_label(p, fmt=lambda x: round(x, 3) if x != 0 else '', label_type='center')
    plt.title(column)
    plt.legend()
    path = f'{path}/image/categorical_compare_{column}{comment}.png'
    plt.savefig(path)
    plt.close()
    return {"image": f'image/categorical_compare_{column}{comment}.png', "title": f'{comment}'}


def gen_multicolumn_lists(dataset, columns, search_column):
    # generate empty data and label lists
    data_list = [pd.Series() for elem in search_column.values() for i in elem]
    label_list = ['' for i in range(len(data_list))]
    # fill prev lists with series object, divided by searching interests
    for elem in columns:
        data_list_new, label_list_new = __split_by_group(dataset.data, elem, search_column,
                                                         method=pd.Series.value_counts,
                                                         method_arg={'dropna': False}, drop=False)
        data_list = [data_list[i].add(data_list_new[i], fill_value=0) for i in range(len(data_list))]
        label_list = label_list_new
    return data_list, label_list


def icd_splitter(series):
    res = pd.Series()
    for key, value in series.items():
        if isinstance(key, str):
            new_key = key.split('.')[0] + "    " + icd.get_description(key.split('.')[0])
        else:
            new_key = key
        if new_key not in res:
            res[new_key] = value
        else:
            res[new_key] += value
    return res
