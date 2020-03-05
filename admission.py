from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import tree

engine = create_engine("mssql+pymssql://ccommittee:teachitbetter@ISTSQL/TMSEPRD")

sql = """ select c.YR_CDE, stage_desc, cast(hist_stage as int) hist_stage, c.id_num
  from STAGE_HISTORY_TRAN c 
  join stage_config sc on c.hist_stage = sc.STAGE
  where datepart(month, HIST_STAGE_DTE) in (10,11,12,1) and
  c.YR_CDE between '2007' and '2020'
  order by YR_CDE ;"""

df = pd.read_sql(sql, engine)

new_df = pd.DataFrame()
target_df = pd.DataFrame()
for i in range(100):
    for year in df.YR_CDE.unique():
        sub_df = df[df['YR_CDE']==year]
        id_nums = pd.Series(sub_df.id_num.unique()).sample(frac=0.7)
        sub_df = sub_df[sub_df['id_num'].isin(id_nums)]
        sub_df = sub_df.drop("id_num", axis=1)
        sub_df['enrollments'] = 0
        sub_df = sub_df.groupby(by=['YR_CDE', 'stage_desc', 'hist_stage']).count()
        sub_df = sub_df.reset_index()
        new_df = new_df.append(sub_df, ignore_index=True, sort=False)

#todo the following line cannot use  YR_CDE as Index
df = new_df.pivot_table(values='enrollments', index=["YR_CDE"], columns=['stage_desc'])
df = df.fillna(value=0.0)
target_df = pd.DataFrame(data={'students': df['Enroll Regular'] + df['Enrolled']})

# print(df[df['stage_desc'] == "Enroll Regular"])



#getting targets
# target_sql = """select c.YR_CDE,
#       count(*) students
#   from STAGE_HISTORY_TRAN c
#
#   where hist_stage in (20, 210) and
#   c.YR_CDE between '2007' and '2019'
#   group by c.YR_CDE
#   order by YR_CDE ;"""

df['students'] = target_df.values
df.corr().to_csv("/Users/emcelroy/enrollment_exploration.csv")
print(df)
df = df.dropna()

# print(df)

classifier = tree.DecisionTreeRegressor()
X = df[['Admit Regular', 'Deposit Regular', 'Application']]
y = df['students']
print(X.shape, y.shape)
classifier.fit(X=X, y=y)
score = classifier.score(X=X,y=y)
print(score)

# print(classifier.predict(X=df[['Inquiry', 'Admit Regular', 'Accepted Admission', 'Application']].iloc[-1:]))