def filter_and_rank(df, cuisine, location, price_bucket, has_delivery=False, sort_by='Score'):
    if df is None or df.empty:
        return df

    filtered = df.copy()

    if cuisine:
        filtered = filtered[filtered['Primary Cuisine'].str.contains(cuisine.lower(), case=False, na=False)]
    if location:
        filtered = filtered[filtered['City'].str.contains(location, case=False, na=False)]
    if price_bucket:
        filtered = filtered[filtered['Price Bucket'] == price_bucket]
    if has_delivery and 'Has Online delivery' in filtered.columns:
        filtered = filtered[filtered['Has Online delivery'] == 1]

    filtered['Score'] = (
        filtered['Aggregate rating'] * 0.7 +
        (filtered['Votes'] / filtered['Votes'].max() if filtered['Votes'].max() > 0 else 0) * 0.3
    )

    if sort_by == 'Rating':
        filtered = filtered.sort_values(by='Aggregate rating', ascending=False)
    elif sort_by == 'Cost':
        filtered = filtered.sort_values(by='Average Cost for two', ascending=True)
    else:
        filtered = filtered.sort_values(by='Score', ascending=False)

    return filtered.head(10)