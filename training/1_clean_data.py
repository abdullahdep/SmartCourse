import pandas as pd

df = pd.read_csv("raw_courses.csv")

print("Original dataset:", df.shape)

# Keep required columns only
required_cols = ["Course Name", "University", "Difficulty Level",
                 "Course Rating", "Course Description", "Department"]

df = df[required_cols]

# Drop missing descriptions
df.dropna(subset=["Course Description"], inplace=True)

# Remove duplicates
df.drop_duplicates(subset=["Course Name", "Course Description"], inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)

df.to_csv("../data/courses_cleaned.csv", index=False)

print("Cleaned dataset saved:", df.shape)
