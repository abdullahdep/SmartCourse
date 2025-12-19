import joblib

# Replace 'your_file.joblib' with the actual path to your file
filename = 'tfidf_vectorizer.joblib'

try:
    # Load the object from the file
    data = joblib.load(filename)

    # Now you can interact with the data in Python
    print(f"Successfully loaded data of type: {type(data)}")

    # You can print a snippet of the data if it's a simple type like a list or dictionary
    # Be cautious with very large objects (like a massive ML model or array), 
    # as printing the whole thing might crash your system.
    if isinstance(data, (list, dict, str, int, float)):
        print("\nSnippet of data:")
        print(str(data)[:500]) # Print first 500 characters/items

    # If it's a machine learning model, you can check its parameters
    if hasattr(data, 'get_params'):
        print("\nModel parameters:")
        print(data.get_params())

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
