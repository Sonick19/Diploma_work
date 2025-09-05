from data import Data
import pandas as pd
from geopy.geocoders import Nominatim
from custom_function import (continuous_data_vis, continuous_compare_vis, kruskal_test,
                             categorical_compare_tc_vis, chi_test)
from html_class import TestRun
from cleaner import clean

# geolocator = Nominatim(user_agent="data2019da")

sample = Data("data/GenomicsOfT1DInUkrai-ALLdeID_DATA_2025-09-02_1901.csv",
              "data/categorical_key_world.txt",
              "data/column_categorization.txt")
sample.apply_func(clean)
# new_data = sample.create_children('patientsex', 'eyecolor')
#
cluster_data = pd.read_csv("data/Sample_Cluster_SuperCluster.csv", sep=';')
cluster_data["Sample"] = cluster_data["Sample"].str.replace('.*_', '', regex=True)
#
sample.data = cluster_data.merge(sample.data, left_on='Sample', right_on='sample_code')
# # new['birthplacelocation'] = new['birthplacelocation'].str.replace('[^|]+рн\.$', '', regex=True)
#
# print(len(new['birthplacelocation'].unique()))
# print(new[['birthplacelocation','SuperCluster', 'Cluster']].head())
# new[['birthplacelocation','SuperCluster', 'Cluster']].to_csv("reference.csv")

# print(sample.data[sample.data['ica_u_ml'].isin(['1:10', '10-Jan', '1:32', '28-05-2025 ', ' -', '>280'])][['sample_code', 'ica_u_ml']])
search = {'SuperCluster': [i for i in range(1,6)]}
# search = {'SuperCluster': [1, 2, 3, 5]}
category_function = {
    (*sample.categorization['continuous_data']['common'], *sample.categorization['continuous_data']['test']):
        [continuous_data_vis(clean=True, comment="Clean data"),
         continuous_compare_vis(clean=True, search_column=search, comment="Clean data"),
         kruskal_test(search, clean=True)
         ],
    (*sample.categorization['numerical_data']['common'], *sample.categorization['numerical_data']['test']):
        [continuous_data_vis(clean=True, comment="Clean data"),
         continuous_compare_vis(clean=True, search_column=search, comment="Clean data"),
         kruskal_test(search, clean=True)
         ],
}
run1 = TestRun("first_one", sample, category_function)
run1.run(only_valuable=True, func=kruskal_test(search, clean=True))
category_function = {
    (*sample.categorization['categorical_data']['common'], *sample.categorization['categorical_data']['test']):
        [categorical_compare_tc_vis(search_column=search),
         chi_test(search_column=search)

         ],
                    }
run2 = TestRun("second_one", sample, category_function)
run2.run(only_valuable=True, func=chi_test(search))