from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


engine = create_engine("mssql+pymssql://ccommittee:teachitbetter@ISTSQL/TMSEPRD")
sql = "select * from student_crs_hist;"

df = pd.read_sql(sql, engine)
df = df[df['BILLING_STS'] == "C"]
df = df[df['YR_CDE'].apply(lambda x:int(x)).between(2016, 2017)]
# df = df[["ADV_REQ_CDE"]]
# print(df)
df = df[['ADV_REQ_CDE', 'YR_CDE']]
df['count'] = 0
df = df.groupby(by=['ADV_REQ_CDE', 'YR_CDE']).count()
df = df.reset_index()
df = df.sort_values(['count'], ascending=False)
df = df[df['count'].between(1,20)]
df = df[~df['ADV_REQ_CDE'].str.startswith("000")]
df = df[~df["ADV_REQ_CDE"].str.startswith('IST', 'RLG')]
# df.answer = df.answer.astype(int)
# df = df.groupby(by="answer").count()
# df = df.set_index('ADV_REQ_CDE')
f = sns.FacetGrid(data=df, col='YR_CDE',col_wrap=2)
f = f.map(sns.barplot, 'ADV_REQ_CDE','count')
# p = sns.barplot(x="ADV_REQ_CDE", y='count', hue="YR_CDE", data=df)
# p.despine(left=True)
# sns.barplot(x=df.index, y="id", data=df)
print(1)
plt.xticks(rotation=90)
plt.title("Student Interest by Advising Code")
plt.savefig("/Users/emcelroy/student_interest.png", dpi=300)
df.to_csv("/Users/emcelroy/student_interest_topic.csv")
print(df.describe(include="all"))

#how do you extend length to show x axis
# * means all columns