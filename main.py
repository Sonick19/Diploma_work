from data import Data
import pandas as pd
from geopy.geocoders import Nominatim
from custom_function import (continuous_data_vis, continuous_compare_vis, kruskal_test,
                             categorical_compare_tc_vis, chi_test, categorical_multicolumn_test,
                             categorical_multicolumn_chi_test, pure_categorical)
from html_class import TestRun
from cleaner import clean
import numpy as np

# geolocator = Nominatim(user_agent="data2019da")

sample = Data("data/GenomicsOfT1DInUkrai-ALLdeID_DATA_2025-09-02_1901.csv",
              "data/categorical_key_world.txt",
              "data/column_categorization.txt")
sample.apply_func(clean)
# new_data = sample.create_children('patientsex', 'eyecolor')
#
cluster_data = pd.read_csv("data/Sample_Cluster_SuperCluster.csv", sep=';')
cluster_data["Sample"] = cluster_data["Sample"].str.replace('.*_', '', regex=True)
sample.data = cluster_data.merge(sample.data, left_on='Sample', right_on='sample_code')
cols = ["ica_u_ml", "gad_65_u_ml", "iaa_u_ml", "ab_ia_2a_u_ml", "ab_znt8ab"]
sample.data["num_antibodies"] = sample.data[cols].notna().sum(axis=1)
sample.data["num_antibodies"] = sample.data["num_antibodies"].apply(lambda row : np.nan if not row else row )
#sample.data["num_antibodies"] = sample.data["ica_u_ml"].notna() + sample.data["gad_65_u_ml"].notna()+sample.data["iaa_u_ml"].notna()+sample.data["ab_ia_2a_u_ml"].notna()+sample.data["ab_znt8ab"].notna()
# print(sample.data[["ica_u_ml", "gad_65_u_ml", "iaa_u_ml", "ab_ia_2a_u_ml", "ab_znt8ab", "num_antibodies"]].head())
# new['birthplacelocation'] = new['birthplacelocation'].str.replace('[^|]+рн\.$', '', regex=True)
#
# print(len(new['birthplacelocation'].unique()))
# print(new[['birthplacelocation','SuperCluster', 'Cluster']].head())
# new[['birthplacelocation','SuperCluster', 'Cluster']].to_csv("reference.csv")
#print(sample.data[sample.data['SuperCluster']==4][['current_date_time','diagnosis_date','ageyears', 'duration_of_disease', 'diabet_onset']])
# print(sample.data[sample.data['ica_u_ml'].isin(['1:10', '10-Jan', '1:32', '28-05-2025 ', ' -', '>280'])][['sample_code', 'ica_u_ml']])


# search = {'SuperCluster': [i for i in range(1,6)]}
search = {'num_antibodies': [i for i in range(1,6)]}
# search = {'casecontrol': [1,2]}

category_function = {
    (*sample.categorization['continuous_data']['common'], *sample.categorization['continuous_data']['test']):
        [continuous_data_vis(clean=True, comment="Clean data"),
         continuous_compare_vis(clean=False, search_column=search, comment="UnClean data"),
         kruskal_test(search, clean=True)
         ],
    (*sample.categorization['numerical_data']['common'], *sample.categorization['numerical_data']['test']):
        [continuous_data_vis(clean=False, comment="Unclean"),
         continuous_compare_vis(clean= False, search_column=search, comment="UnClean data"),
         kruskal_test(search, clean=True)
         ],
}
# run1 = TestRun("numerical_data", sample, category_function)
# # run1.run(only_valuable=True, func=kruskal_test(search, clean=True))
# run1.run()


category_function = {
    (*sample.categorization['categorical_data']['common'], *sample.categorization['categorical_data']['test']):
        [categorical_compare_tc_vis(search_column=search),
         chi_test(search_column=search)

         ],
                   }
run2 = TestRun("categorical_data_clean", sample, category_function)
run2.run()
# run2.run(only_valuable=True, func=chi_test(search))
# category_function = {
#     (*sample.categorization['categorical_data']['common'], *sample.categorization['categorical_data']['test']):
#         [pure_categorical()
#          ],
#                    }
# run5 = TestRun("pure_categorical_data_clean", sample, category_function)
# run5.run()

#
# category_function = {
#     (tuple(*sample.categorization['diseases_data']['test']),):
#         [categorical_multicolumn_test(search_column=search, mod=True),
#          categorical_multicolumn_chi_test(search_column=search, mod=True, hide=True),
#          categorical_multicolumn_test(search_column=search, ),
#          categorical_multicolumn_chi_test(search_column=search, hide=True)
#          ]
# }
#
# run3 = TestRun("t1_complication", sample, category_function )
# run3.run()

# category_function = {
#     (*sample.categorization['checkbox_data']['sub_ethnos'],
#      *sample.categorization['checkbox_data']['ethnic_group'],
#      *sample.categorization['checkbox_data']['mother_twins_4'],
#      *sample.categorization['checkbox_data']['family_t1d_who'],
#      *sample.categorization['checkbox_data']['chronic_autoimmune_diseases'],
#      *sample.categorization['checkbox_data']['family_ai_specify'],
#
#      ):
#         [categorical_compare_tc_vis(search_column=search),
#          chi_test(search_column=search)
#
#          ],
#                    }
# run4 = TestRun("checkbox_data_clean", sample, category_function)
# run4.run(only_valuable=True, func=chi_test(search))

# write = sample.data[sample.data['casecontrol']==1][['SuperCluster', 'ageyears', 'patientsex',
#                      'trade_name_prandial_insulin', 'c_peptide_levels_ng_ml',
#                     'hba1c_results_1','hba1c_results_2',
#                      ]]
# write.to_csv('to_powerBi.csv')