import pandas as pd

df = pd.read_csv('data/manabifun_questions.csv')
print(f'Total questions: {len(df)}')
print(f'Topics: {df["topic"].unique()}')
print(f'Difficulties: {df["difficulty"].unique()}')
print('Questions by topic and difficulty:')
print(df.groupby(['topic', 'difficulty']).size())