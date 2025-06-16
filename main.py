import pandas as pd
import os
import utils
import database

df = pd.DataFrame(columns=['invoice_date', 'supplier', 'description', 'amount', 'currency'])

for folder in sorted(os.listdir("./invoices")):
    folder_dir = os.path.join("./invoices", folder)

    for file in os.listdir(folder_dir):
        pdf_dir = os.path.join(folder_dir, file)
        print(f"📃 Processing invoice: {pdf_dir}")

        try:
            text = utils.extract_pdf_text(pdf_dir)
            csv_file = utils.send_content_to_model(text)
            invoice_df = utils.convert_csv_to_dataframe(csv_file)

            df = pd.concat([df, invoice_df], ignore_index=True)
            df.to_csv("./data/invoices.csv")

        except Exception as e:
            print(f"Error processing {pdf_dir}: {e}")

if not df.empty:
    succes = database.save_to_database(df)
    if succes:
         print(f"✅ Successfully saved {len(df)} invoices to database")
    else:
        print("❌ Failed to save data to database")
else:
    print("No invoice data to save")