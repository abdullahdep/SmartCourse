import pandas as pd

df = pd.read_csv("raw_courses.csv", encoding='latin-1')

print("Original dataset:", df.shape)

# Keep required columns only
required_cols = ["Department", "University", "City/Cities",
                 "Marks required", "Labs Avalible", "Course Description" ,"Admission dates" ,"shifts","online" ,"Course title"]

df = df[required_cols]

# Drop missing descriptions
df.dropna(subset=["Course Description"], inplace=True)

# Remove duplicates
df.drop_duplicates(subset=["Course title", "Course Description"], inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)

df.to_csv("../data/courses_cleaned.csv", index=False)

print("Cleaned dataset saved:", df.shape)
