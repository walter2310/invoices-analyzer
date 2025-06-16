import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./data/invoices.csv")

def generate_bar_plot(df):
    grouped = df.groupby('supplier')['amount'].sum().sort_values()

    plt.figure(figsize=(16, 6))
    plt.barh(grouped.index, grouped.values)

    plt.xlabel("Total Amount")
    plt.ylabel("Service Providers")
    plt.title("Total Amount by Service Provider")

    for index, value in enumerate(grouped.values):
        plt.text(value, index, f" {value:,.2f}")

    plt.tight_layout()
    plt.show()


def generate_bar_plot_by_month(df):
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%d/%m/%Y")
    df["year_month"] = df["invoice_date"].dt.to_period("M")

    grouped = df.groupby("year_month")["amount"].sum()
    plt.figure(figsize=(16, 6))
    bars = plt.bar(grouped.index.astype(str), grouped.values)

    plt.xlabel("Total Amount")
    plt.ylabel("Months")
    plt.title("Total Amount by Month")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:,.2f}',
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def generate_table_with_expensives(df):
    top_5 = df.nlargest(5, 'amount')[['supplier', 'amount', 'currency']]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off')

    table_data = []
    for _, row in top_5.iterrows():
        table_data.append([
            row['supplier'],
            f"${row['amount']:,.2f}",
        ])

    columns = ['Supplier', 'Amount', 'Currency']
    table = ax.table(
        cellText=table_data,
        colLabels=columns,
        loc='center',
        cellLoc='center',
        colColours=['#f0f0f0'] * 3
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    plt.title("Top 5 Most Expensive Invoices", pad=20, fontsize=14, fontweight='bold')
    plt.show()


def average_expense_by_month(df):
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%d/%m/%Y")
    df["year_month"] = df["invoice_date"].dt.to_period("M")

    monthly_count = df.groupby("year_month")["amount"].count()
    monthly_sum = df.groupby("year_month")["amount"].sum()

    monthly_average = round(monthly_sum / monthly_count, 2)
    return monthly_average


def plot_average_expenses(monthly_avg):
    plt.figure(figsize=(10, 5))
    monthly_avg.plot(kind='bar', color='skyblue')
    plt.title("Promedio de Gastos Mensuales")
    plt.xlabel("Mes")
    plt.ylabel("Gasto Promedio (USD)")

    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
