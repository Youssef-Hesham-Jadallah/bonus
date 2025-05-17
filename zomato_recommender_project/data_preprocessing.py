import pandas as pd
import os

def classify_cost(cost):
    if cost <= 500:
        return 'Low'
    elif cost <= 1500:
        return 'Medium'
    else:
        return 'High'

def load_and_clean_data(path):
    try:
        if not os.path.exists(path):
            print(f"❌ Error: File not found at {path}. Please check the file path.")
            return None

        try:
            df = pd.read_csv(path, encoding='latin-1')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(path, encoding='ISO-8859-1')

        drop_cols = ['Switch to order menu', 'Currency', 'Rating color', 'Rating text', 'Address']
        df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

        df.drop_duplicates(inplace=True)
        df.dropna(subset=['Restaurant Name', 'Cuisines', 'Average Cost for two', 'Aggregate rating', 'City', 'Locality'], inplace=True)

        df['Cuisines'] = df['Cuisines'].str.lower().str.strip()
        df['Primary Cuisine'] = df['Cuisines'].apply(lambda x: x.split(',')[0] if ',' in x else x)

        df['Price Bucket'] = df['Average Cost for two'].apply(classify_cost)

        for col in ['Has Table booking', 'Has Online delivery', 'Is delivering now']:
            if col in df.columns:
                df[col] = df[col].map({'Yes': 1, 'No': 0})

        df['Aggregate rating'] = df['Aggregate rating'].apply(lambda x: min(5.0, max(0.0, x)))

        df['City'] = df['City'].str.strip()
        df['Locality'] = df['Locality'].str.strip()

        return df

    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return None

if __name__ == "__main__":
    test_path = "data/zomato.csv"
    cleaned_data = load_and_clean_data(test_path)
    if cleaned_data is not None:
        print("✅ Data loaded successfully. Sample:")
        print(cleaned_data.head())
    else:
        print("❌ Failed to load or clean the data.")