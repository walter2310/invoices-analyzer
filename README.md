# Invoice Analysis System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/pandas-1.3%2B-orange)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.4%2B-blueviolet)

A solution for processing, analyzing, and visualizing invoice data with automated PDF reporting capabilities.

## Features

- 📄 **Invoice Processing**
  - Extract structured data from raw invoice PDFs
  - Handle multiple date formats and currencies

- 📊 **Data Analysis**
  - Monthly spending trends
  - Vendor expenditure analysis
  - Top expense identification
  - Average monthly spending calculations

- 📈 **Visualization**
  - Interactive dashboard generation
  - Automated PDF reports

- 🔄 **Workflow Automation**
  - Batch processing of multiple invoices
  - Scheduled report generation
  - Email notification system (optional)

## Requirements

- **Python**: 3.11.7 (recommended)
- **Docker**: Required to run the project containers
- **Docker Containers**:
  - PostgreSQL: `docker pull postgres:15.3`
  - pgAdmin 4 (optional): `docker pull dpage/pgadmin4`

## Dependencies

- Python 3.11.7+
- pandas
- matplotlib
- PyMuPDF (fitz)

## Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/invoice-analysis.git
cd invoice-analysis
```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Donwload docker containers:**
    ```sh
    docker pull postgres:15.3
    ```

     ```sh
    docker pull dpage/pgadmin4
    ```

4. **Docker compose:**
    ```sh
    docker compose up -d
    ```
