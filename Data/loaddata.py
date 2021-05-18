#Pre req

import numpy as np
import pandas as pd
from collections import Counter
import os

import requests


"""#Helper functions"""

def checkduplicates(series1, series2):
  a = list(series1.unique())
  b = list(series2.unique())

  cols = list(set(a + b))
  cols.sort()
  d = []
  c = []
  for i in cols:
    if i in a and i in b:
      c.append(1)
      d.append(1)
    if i not in a and i in b:
      c.append(0)
      d.append(1)
    if i in a and i not in b:
      c.append(1)
      d.append(0)

  thedf = pd.DataFrame(data =[c, d], columns=cols)
  return thedf.transpose()

def convertIndianSep(num):
  a = str(num).split('.')

  if len(a[0]) > 3:
    b = a[0][0:len(a[0])-3]
    c = ',' + a[0][len(a[0])-3:len(a[0])]
    if len(b)%2 == 0:
      d = ','.join(b[i:i + 2] for i in range(0, len(b), 2))
    else:
      val = b[1:len(b)]
      d = b[0] +',' + ','.join(val[i:i + 2] for i in range(0, len(val), 2))
    retrunval = d + c
    if len(a) == 2:
      retrunval = d + c
    if int(retrunval.replace(',', '')) != int(a[0]):
      print('error in conversion')
    return retrunval + '.' + a[1]
  else:
    return num

"""#Loading required data

#Download required data of 2016, 19 and 21 elections
"""
URLS = ['https://raw.githubusercontent.com/Mikail1010/TN_Election_Analysis/main/Data/2021/Const_wise_sum_21_S22.csv',
'https://github.com/Mikail1010/TN_Election_Analysis/raw/main/Data/2016/Detailed%20Results.xlsx',
'https://github.com/Mikail1010/TN_Election_Analysis/raw/main/Data/2016/List%20Of%20Political%20Parties%20Participated.xlsx',
'https://raw.githubusercontent.com/Mikail1010/TN_Election_Analysis/main/Data/2019/Results_summary_for_2019.csv',
'https://raw.githubusercontent.com/Mikail1010/TN_Election_Analysis/main/Data/2019/PA_AC_2019.csv',
'https://raw.githubusercontent.com/Mikail1010/TN_Election_Analysis/main/Data/2019/Const_wise_sum_19_S22.csv',
'https://raw.githubusercontent.com/Mikail1010/TN_Election_Analysis/main/Data/2019/PC_Const_wise_sum_19_S22.csv',
'https://raw.githubusercontent.com/Mikail1010/TN_Election_Analysis/main/Data/2019/List%20Of%20Political%20Parties%20Participated_19.csv',
'https://raw.githubusercontent.com/Mikail1010/TN_Election_Analysis/main/Data/Alliance.csv',]





for url in URLS:
	r = requests.get(url, allow_redirects=True)
	filename = url.rsplit('/',1)[1].replace('%20', ' ')
	open(filename, 'wb').write(r.content)


"""Load other useful data"""

AllianceDict = pd.read_csv("Alliance.csv", index_col=0).to_dict()
AllianceDict_2021 = AllianceDict['2021']
AllianceDict_2019 = AllianceDict['2019']
AllianceDict_2016 = AllianceDict['2016']

# """#2021"""

Cons_result_2021 = pd.read_csv("Const_wise_sum_21_S22.csv")
Cons_result_2021.drop(["O.S.N.", "EVM Votes", "Postal Votes"], axis=1, inplace=True)
Cons_result_2021['Total Votes'] = Cons_result_2021['Total Votes'].astype(int)

Cons_result_2021.replace("\n", " ", inplace=True, regex=True)
Cons_result_2021.replace("   ", " ", inplace=True, regex=True)
Cons_result_2021['Party'] = Cons_result_2021['Party'].str.strip()
Cons_result_2021.replace("  ", " ", inplace=True, regex=True)

Cons_result_2021=Cons_result_2021.rename(columns = {'Constituency':'AC Name'})

Cons_result_2021["All_21"] = Cons_result_2021["Party"].apply(lambda x: AllianceDict_2021.get(x, "NonA"))
Cons_result_2021["All_19"] = Cons_result_2021["Party"].apply(lambda x: AllianceDict_2019.get(x, "NonA"))
Cons_result_2021["All_16"] = Cons_result_2021["Party"].apply(lambda x: AllianceDict_2016.get(x, "NonA"))


"""#2019"""

Party_list_2019 = pd.read_csv("List Of Political Parties Participated_19.csv")
Party_list_2019.drop(["PARTY TYPE", "Sr.No."], axis=1, inplace=True)

Party_list_2019.replace("\n", " ", inplace=True, regex=True)
Party_list_2019['ABBREVIATION'] = Party_list_2019['ABBREVIATION'].str.strip()
Party_list_2019['PARTY NAME'] = Party_list_2019['PARTY NAME'].str.strip()
Party_list_2019.replace("  ", " ", inplace=True, regex=True)

Party_dict_2019 = dict(zip(Party_list_2019["ABBREVIATION"], Party_list_2019["PARTY NAME"]))

Cons_result_2019 = pd.read_csv("Const_wise_sum_19_S22.csv")

Total_Votes_state_2019 = Cons_result_2019["TOTAL VOTES IN STATE"].unique()[0]

Cons_result_2019.drop(["State-UT Code & Name", "PC NO", "AC NO", "TOTAL VOTES IN STATE"], axis=1, inplace=True)

Cons_result_2019.replace("\n", " ", inplace=True, regex=True)
Cons_result_2019['PC NAME'] = Cons_result_2019['PC NAME'].str.strip()
Cons_result_2019['AC NAME'] = Cons_result_2019['AC NAME'].str.strip()
Cons_result_2019['PARTY'] = Cons_result_2019['PARTY'].str.strip()
Cons_result_2019.replace("  ", " ", inplace=True, regex=True)
Cons_result_2019['PARTY'].replace("  ", " ", inplace=True, regex=True)

Cons_result_2019["Party"] = Cons_result_2019["PARTY"].apply(lambda x: Party_dict_2019[x])
Cons_result_2019.drop(["PARTY"], axis=1, inplace=True)

old_const_name = ["Avanashi (SC)","Colachel","Dharapuram (SC)","Gandharvakottai","Kattumannarkoil(SC)","Pappireddippatti","Sholingur","Tittagudi (SC)", "Vridhachalam"]
new_const_name = ["Avanashi", "Colachal","Dharapuram","Gandarvakkottai","Kattumannarkoil", "Pappireddipatti","Sholinghur","Tittakudi","Vriddhachalam"]
Cons_result_2019.replace(old_const_name, new_const_name, inplace=True, regex=False)

Cons_result_2019=Cons_result_2019.rename(columns = {'AC NAME':'AC Name', 'PC NAME':'PC Name', 'CANDIDATE NAME':'Candidate'})


"""Removing the NOTA column and adding it as a row for each AC

Extacting total votes in C and saving it in a dict
"""

NOTA_list_2019 = Cons_result_2019[["AC Name", "NOTA VOTES EVM"]].copy(deep=True)
NOTA_list_2019.drop_duplicates(inplace=True)
NOTA_dict_2019 = dict(zip(NOTA_list_2019["AC Name"], NOTA_list_2019["NOTA VOTES EVM"]))

ACPC_list_2019 = Cons_result_2019[["AC Name", "PC Name"]].copy(deep=True)
ACPC_list_2019.drop_duplicates(inplace=True)
ACPC_dict_2019 = dict(zip(ACPC_list_2019["AC Name"], ACPC_list_2019["PC Name"]))


"""Adding PC. Run this after running 2019 ACPC_dict_2019"""

Cons_result_2021['PC Name'] = Cons_result_2021['AC Name'].apply(lambda x:  ACPC_dict_2019.get(x, "Check"))
Cons_result_2021.sort_values(['PC Name', 'AC Name', 'Total Votes'], ascending=[True, True, False], inplace=True)
Cons_result_2021 = Cons_result_2021.reindex(columns=['PC Name', 'AC Name', 'Candidate', 'Party', 'Total Votes', '% of Votes','All_21', 'All_19', 'All_16'])


AC_electors_list_2019 = Cons_result_2019[["AC Name", "TOTAL ELECTORS"]].copy(deep=True)
AC_electors_list_2019.drop_duplicates(inplace=True)
AC_electors_dict_2019 = dict(zip(AC_electors_list_2019["AC Name"], AC_electors_list_2019["TOTAL ELECTORS"]))

Nota_rows = []
for i in Cons_result_2019["AC Name"].unique():
  Nota_rows.append([ACPC_dict_2019[i], i, AC_electors_dict_2019[i], 0, 'NOTA', NOTA_dict_2019[i], 'None of the Above'])
Nota_df = pd.DataFrame(Nota_rows, columns=Cons_result_2019.columns)

Cons_result_2019 = Cons_result_2019.append(Nota_df, ignore_index=True)
Cons_result_2019.drop(["NOTA VOTES EVM", "TOTAL ELECTORS"], axis=1, inplace=True)


"""Adding postal votes"""

PC_postal_Cons_result_2019 = pd.read_csv("PC_Const_wise_sum_19_S22.csv")
PC_postal_Cons_result_2019.replace("\n", " ", inplace=True, regex=True)
PC_postal_Cons_result_2019[' PC NAME '] = PC_postal_Cons_result_2019[' PC NAME '].str.strip()

PostVotesdict = {}
for i in Cons_result_2019['Candidate'].unique():
  if i != "NOTA":
    PostVotesdict[i] = PC_postal_Cons_result_2019[PC_postal_Cons_result_2019[" CANDIDATES NAME "] == i][" POSTAL "].values[0]
val = PC_postal_Cons_result_2019[PC_postal_Cons_result_2019[" CANDIDATES NAME "] == "NOTA"]
for i in val.index:
  PostVotesdict["NOTA" + val.loc[i][" PC NAME "]] = val.loc[i][" POSTAL "]

PCinACsdict = {}
a = Cons_result_2019.copy(deep=True)
a.drop_duplicates(['AC Name'], inplace=True)

for i in a["PC Name"].unique():
  PCinACsdict[i] = len(a[a["PC Name"] == i])

import math
def trouble(x1, x2, x3):
  occ = PCinACsdict[x1]
  if x3 != "NOTA":
    tot = PostVotesdict[x3]
  elif x3 == "NOTA":
    tot = PostVotesdict["NOTA" + x1]
  return math.floor(tot/occ)

Cons_result_2019['Postal votes'] = Cons_result_2019.apply(lambda x: trouble(x["PC Name"], x["AC Name"], x["Candidate"]), axis=1)

Cons_result_2019["Total Votes"] = Cons_result_2019["VOTES SECURED EVM"] + Cons_result_2019['Postal votes']
Cons_result_2019.drop(["VOTES SECURED EVM", "Postal votes"], axis=1, inplace=True)
Cons_result_2019.sort_values(['PC Name', 'AC Name', 'Total Votes'], ascending=[True, True, False], inplace=True)


AC_TotalElectors_2019 = Cons_result_2019.groupby(['AC Name'])['Total Votes'].sum()
Cons_result_2019["TE"] = Cons_result_2019["AC Name"].apply(lambda x: AC_TotalElectors_2019[x])
Cons_result_2019["% of Votes"] = Cons_result_2019['Total Votes'] * 100 / Cons_result_2019["TE"]

Cons_result_2019["All_21"] = Cons_result_2019["Party"].apply(lambda x: AllianceDict_2021.get(x, "NonA"))
Cons_result_2019["All_19"] = Cons_result_2019["Party"].apply(lambda x: AllianceDict_2019.get(x, "NonA"))
Cons_result_2019["All_16"] = Cons_result_2019["Party"].apply(lambda x: AllianceDict_2016.get(x, "NonA"))

"""#2016"""

Party_list_2016 = pd.read_excel("List Of Political Parties Participated.xlsx", header=1)
Party_list_2016.drop(["Party Type", "Unnamed: 3"], axis=1, inplace=True)

Party_list_2016.replace("\n", " ", inplace=True, regex=True)
Party_list_2016['Party Abbreviation'] = Party_list_2016['Party Abbreviation'].str.strip()
Party_list_2016['Party Name'] = Party_list_2016['Party Name'].str.strip()
Party_list_2016.replace("  ", " ", inplace=True, regex=True)

Party_dict_2016 = dict(zip(Party_list_2016["Party Abbreviation"], Party_list_2016["Party Name"]))


Cons_result_2016 = pd.read_excel("Detailed Results.xlsx", header=2)
Cons_result_2016.drop(["Constituency No.", "Candidate Sex", "Candidate Age", "Candidate Category", " VALID VOTES POLLED in General", " VALID VOTES POLLED in Postal", "Total Electors"], axis=1, inplace=True)
Cons_result_2016["% of Votes"] = round((Cons_result_2016[" Total Valid Votes"] / Cons_result_2016["Total Votes"]) * 100, 2)
Cons_result_2016["Party"] = Cons_result_2016[" Party Name"].apply(lambda x: Party_dict_2016[x])
Cons_result_2016.drop(["Total Votes", " Party Name"], axis=1, inplace=True)

Cons_result_2016=Cons_result_2016.rename(columns = {'Constituency Name':'AC Name', 'Candidate Name':'Candidate', ' Total Valid Votes':'Total Votes'})

No_election_2016 = ["Thanjavur", "Aravakurichi"]
Cons_result_2016['Total Votes'].fillna(0, inplace=True)
Cons_result_2016['Total Votes'] = Cons_result_2016['Total Votes'].astype(int)


Cons_result_2016.replace("\n", " ", inplace=True, regex=True)
Cons_result_2016['Party'] = Cons_result_2016['Party'].str.strip()
Cons_result_2016['AC Name'] = Cons_result_2016['AC Name'].str.strip()
Cons_result_2016.replace("  ", " ", inplace=True, regex=True)

old_party_name = ["Republican Party of India (A)", "ALL PENSIONER'S PARTY", "Shivsena"]
new_party_name = ["Republican Party of India (Athawale)", "All Pensioner’s Party", "Shiv Sena"]

Cons_result_2016.replace(old_party_name, new_party_name, inplace=True, regex=False)
Cons_result_2016.replace(old_const_name, new_const_name, inplace=True, regex=False)


Cons_result_2016['PC Name'] = Cons_result_2016['AC Name'].apply(lambda x:  ACPC_dict_2019.get(x, "Check"))
Cons_result_2016.sort_values(['PC Name', 'AC Name', 'Total Votes'], ascending=[True, True, False], inplace=True)

Cons_result_2016["All_21"] = Cons_result_2016["Party"].apply(lambda x: AllianceDict_2021.get(x, "NonA"))
Cons_result_2016["All_19"] = Cons_result_2016["Party"].apply(lambda x: AllianceDict_2019.get(x, "NonA"))
Cons_result_2016["All_16"] = Cons_result_2016["Party"].apply(lambda x: AllianceDict_2016.get(x, "NonA"))
Cons_result_2016 = Cons_result_2016.reindex(columns=Cons_result_2021.columns)

print('16, 19 and 21 Election results dataframe: Cons_result_2016, Cons_result_2019, Cons_result_2021')
print('PC to AC constitunecy conversion dict ACPC_dict_2019')
print('No of AC in each PC dict (2019) PCinACsdict ')
print('AC electors details for 19 AC_electors_dict_2019')


