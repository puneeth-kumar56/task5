import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

print("Sales Data Analysis Notebook")
print("=" * 50)

# Step 1: Create Sample Sales Data (if no CSV file is provided)
def create_sample_data():
    """Create sample sales data for demonstration"""
    np.random.seed(42)
    
    # Generate sample data
    n_records = 1000
    
    # Product categories and names
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports']
    products = {
        'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Camera'],
        'Clothing': ['Shirt', 'Pants', 'Dress', 'Shoes', 'Jacket'],
        'Home & Garden': ['Chair', 'Table', 'Lamp', 'Plant', 'Vase'],
        'Books': ['Fiction', 'Non-Fiction', 'Textbook', 'Magazine', 'Comic'],
        'Sports': ['Ball', 'Racket', 'Shoes', 'Equipment', 'Apparel']
    }
    
    # Generate dates for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    data = []
    for i in range(n_records):
        category = np.random.choice(categories)
        product = np.random.choice(products[category])
        
        # Generate realistic sales data
        base_price = np.random.uniform(10, 500)
        quantity = np.random.randint(1, 10)
        discount = np.random.uniform(0, 0.3) if np.random.random() > 0.7 else 0
        
        # Random date within the last year
        random_date = start_date + timedelta(days=np.random.randint(0, 365))
        
        # Customer regions
        regions = ['North', 'South', 'East', 'West', 'Central']
        region = np.random.choice(regions)
        
        # Sales rep
        sales_reps = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
        sales_rep = np.random.choice(sales_reps)
        
        record = {
            'Date': random_date.strftime('%Y-%m-%d'),
            'Product': product,
            'Category': category,
            'Quantity': quantity,
            'Unit_Price': round(base_price, 2),
            'Discount': round(discount, 3),
            'Region': region,
            'Sales_Rep': sales_rep,
            'Total_Sale': round(base_price * quantity * (1 - discount), 2)
        }
        data.append(record)
    
    return pd.DataFrame(data)

# Step 2: Load or Create Data
print("\n1. Loading Sales Data")
print("-" * 30)

# Try to load from CSV file, otherwise create sample data
try:
    # If you have a CSV file, replace 'sales_data.csv' with your file path
    df = pd.read_csv('sales_data.csv')
    print("✓ CSV file loaded successfully!")
except FileNotFoundError:
    print("Creating sample sales data for demonstration...")
    df = create_sample_data()
    print("✓ Sample data created successfully!")

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Display basic information about the dataset
print(f"\nDataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nBasic statistics:")
print(df.describe())

# Step 3: Data Analysis using groupby(), sum(), and other operations
print("\n\n2. Data Analysis")
print("-" * 30)

# Analysis 1: Sales by Category
print("\n📊 Sales by Category:")
category_sales = df.groupby('Category')['Total_Sale'].agg(['sum', 'mean', 'count']).round(2)
category_sales.columns = ['Total_Sales', 'Average_Sale', 'Number_of_Sales']
category_sales = category_sales.sort_values('Total_Sales', ascending=False)
print(category_sales)

# Analysis 2: Sales by Region
print("\n📊 Sales by Region:")
region_sales = df.groupby('Region')['Total_Sale'].agg(['sum', 'mean', 'count']).round(2)
region_sales.columns = ['Total_Sales', 'Average_Sale', 'Number_of_Sales']
region_sales = region_sales.sort_values('Total_Sales', ascending=False)
print(region_sales)

# Analysis 3: Top Performing Sales Representatives
print("\n📊 Top Sales Representatives:")
rep_performance = df.groupby('Sales_Rep')['Total_Sale'].agg(['sum', 'count', 'mean']).round(2)
rep_performance.columns = ['Total_Sales', 'Number_of_Sales', 'Average_Sale']
rep_performance = rep_performance.sort_values('Total_Sales', ascending=False)
print(rep_performance)

# Analysis 4: Monthly Sales Trend
print("\n📊 Monthly Sales Trend:")
df['Month'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Total_Sale'].sum().round(2)
print(monthly_sales)

# Analysis 5: Product Performance
print("\n📊 Top 10 Products by Sales:")
product_sales = df.groupby(['Category', 'Product'])['Total_Sale'].sum().round(2)
top_products = product_sales.sort_values(ascending=False).head(10)
print(top_products)

# Analysis 6: Discount Impact Analysis
print("\n📊 Discount Impact Analysis:")
discount_analysis = df.groupby(pd.cut(df['Discount'], bins=[0, 0.1, 0.2, 0.3], labels=['Low (0-10%)', 'Medium (10-20%)', 'High (20-30%)']))['Total_Sale'].agg(['mean', 'count']).round(2)
print(discount_analysis)

# Step 4: Advanced Analysis
print("\n\n3. Advanced Analysis")
print("-" * 30)

# Correlation analysis
print("\n📊 Correlation Analysis:")
numeric_cols = ['Quantity', 'Unit_Price', 'Discount', 'Total_Sale']
correlation_matrix = df[numeric_cols].corr().round(3)
print(correlation_matrix)

# Category and Region cross-analysis
print("\n📊 Sales by Category and Region:")
pivot_table = pd.pivot_table(df, values='Total_Sale', index='Category', columns='Region', aggfunc='sum', fill_value=0).round(2)
print(pivot_table)

# Step 5: Key Insights
print("\n\n4. Key Insights")
print("-" * 30)

total_revenue = df['Total_Sale'].sum()
total_transactions = len(df)
avg_transaction = df['Total_Sale'].mean()
best_category = category_sales.index[0]
best_region = region_sales.index[0]
best_rep = rep_performance.index[0]

print(f"💰 Total Revenue: ${total_revenue:,.2f}")
print(f"🛒 Total Transactions: {total_transactions:,}")
print(f"📈 Average Transaction Value: ${avg_transaction:.2f}")
print(f"🏆 Best Category: {best_category} (${category_sales.loc[best_category, 'Total_Sales']:,.2f})")
print(f"🌍 Best Region: {best_region} (${region_sales.loc[best_region, 'Total_Sales']:,.2f})")
print(f"👤 Top Sales Rep: {best_rep} (${rep_performance.loc[best_rep, 'Total_Sales']:,.2f})")

# Calculate growth metrics if we have time series data
if len(monthly_sales) > 1:
    latest_month = monthly_sales.iloc[-1]
    previous_month = monthly_sales.iloc[-2]
    growth_rate = ((latest_month - previous_month) / previous_month) * 100
    print(f"📊 Month-over-Month Growth: {growth_rate:.1f}%")

print("\n\n5. Creating Visualizations")
print("-" * 30)

# Create visualizations
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Sales Data Analysis Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Sales by Category (Bar Chart)
category_sales['Total_Sales'].plot(kind='bar', ax=axes[0,0], color='skyblue')
axes[0,0].set_title('Total Sales by Category')
axes[0,0].set_xlabel('Category')
axes[0,0].set_ylabel('Total Sales ($)')
axes[0,0].tick_params(axis='x', rotation=45)

# Plot 2: Sales by Region (Pie Chart)
axes[0,1].pie(region_sales['Total_Sales'], labels=region_sales.index, autopct='%1.1f%%')
axes[0,1].set_title('Sales Distribution by Region')

# Plot 3: Monthly Sales Trend (Line Chart)
monthly_sales.plot(kind='line', ax=axes[0,2], marker='o', color='green')
axes[0,2].set_title('Monthly Sales Trend')
axes[0,2].set_xlabel('Month')
axes[0,2].set_ylabel('Total Sales ($)')
axes[0,2].tick_params(axis='x', rotation=45)

# Plot 4: Sales Rep Performance (Horizontal Bar Chart)
rep_performance['Total_Sales'].plot(kind='barh', ax=axes[1,0], color='orange')
axes[1,0].set_title('Sales Rep Performance')
axes[1,0].set_xlabel('Total Sales ($)')

# Plot 5: Price vs Quantity Scatter Plot
axes[1,1].scatter(df['Unit_Price'], df['Quantity'], alpha=0.6, c=df['Total_Sale'], cmap='viridis')
axes[1,1].set_title('Price vs Quantity (colored by Total Sale)')
axes[1,1].set_xlabel('Unit Price ($)')
axes[1,1].set_ylabel('Quantity')

# Plot 6: Discount Distribution (Histogram)
axes[1,2].hist(df['Discount'], bins=20, edgecolor='black', alpha=0.7, color='purple')
axes[1,2].set_title('Discount Distribution')
axes[1,2].set_xlabel('Discount Rate')
axes[1,2].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

print("✓ Visualizations created successfully!")

# Step 6: Export Results
print("\n\n6. Exporting Results")
print("-" * 30)

# Create summary report
summary_data = {
    'Metric': [
        'Total Revenue',
        'Total Transactions',
        'Average Transaction Value',
        'Best Category',
        'Best Region',
        'Top Sales Rep'
    ],
    'Value': [
        f"${total_revenue:,.2f}",
        f"{total_transactions:,}",
        f"${avg_transaction:.2f}",
        best_category,
        best_region,
        best_rep
    ]
}

summary_df = pd.DataFrame(summary_data)

# Save analysis results
try:
    # Export summary
    summary_df.to_csv('sales_analysis_summary.csv', index=False)
    
    # Export detailed analysis
    category_sales.to_csv('category_analysis.csv')
    region_sales.to_csv('region_analysis.csv')
    rep_performance.to_csv('sales_rep_performance.csv')
    
    print("✓ Analysis results exported to CSV files!")
    print("  - sales_analysis_summary.csv")
    print("  - category_analysis.csv")
    print("  - region_analysis.csv")
    print("  - sales_rep_performance.csv")
    
except Exception as e:
    print(f"Note: Could not export files (this is normal in some environments): {e}")

print("\n" + "="*50)
print("Analysis Complete! 🎉")
print("="*50)

# Display final summary
print("\n📋 EXECUTIVE SUMMARY")
print("-" * 20)
print(summary_df.to_string(index=False))

print(f"""
🔍 KEY FINDINGS:
• {best_category} is our strongest category with ${category_sales.loc[best_category, 'Total_Sales']:,.2f} in sales
• {best_region} region leads in performance with ${region_sales.loc[best_region, 'Total_Sales']:,.2f}
• {best_rep} is our top sales representative with ${rep_performance.loc[best_rep, 'Total_Sales']:,.2f} in sales
• Average transaction value is ${avg_transaction:.2f}
• Total of {total_transactions:,} transactions generated ${total_revenue:,.2f} in revenue
""")
