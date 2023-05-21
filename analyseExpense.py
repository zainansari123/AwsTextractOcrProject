
from aws_config import *



# Step:1 => Convert Pdf to Image, Working on first image extracted
convertpdf2image()
print('Step 1 complete')

def process_expense_analysis(client):
    with open(r"Page_1.jpg", 'rb') as image:
        img=bytearray(image.read())

    response = client.analyze_expense(Document={'Bytes':img}) # Analyze document
    print('Step 2 complete, Api Success')

    for expense_doc in response["ExpenseDocuments"]:
        for line_item_group in expense_doc["LineItemGroups"]:
            for line_items in line_item_group["LineItems"]:
                for expense_fields in line_items["LineItemExpenseFields"]:
                    print_labels_and_values(expense_fields)
                    # print()

        for summary_field in expense_doc["SummaryFields"]:
            print_labels_and_values(summary_field)
            # print()
    outPutFile(FinalData,"Today/final_modified_{}.json".format(output_filename))
    outPutFile(rawData,"Today/raw_{}.json".format(output_filename))
    
    print('Step 3 complete, Output Success')

    

def main():
    client = boto3.client("textract",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,region_name=REGION)
    process_expense_analysis(client)

if __name__ == "__main__":
    main()

                  