import fitz
import pandas as pd


def get_raw_text(filepath):
    """
        Currently only handle pdf document with one page.
    """
    doc = fitz.open(filepath)
    raw_text = ''
    for do in doc:
        raw_text += do.getText()
    
    print('raw')
    print(raw_text)
    return raw_text


def get_clean_text_list(raw_text):
    clean_text_list = [str(s.replace(u"\u2022", u""))
                       .strip()
                       for s in raw_text.split("\n")]
    clean_text_list = [s for s in clean_text_list if s != ""]
    return clean_text_list


def get_bank_account_data(clean_text_list):
    bank_account = None
    for text in clean_text_list:
        if "NO. REKENING" in text:
            bank_account = str(text.split(" : ")[1])
            break
    bank_account_data = dict(bank_account=bank_account)
    return bank_account_data


def get_transaction_summary(clean_text_list):
    initial_balance = None
    credit_mutation = None
    credit_count = None
    debit_mutation = None
    debit_count = None
    final_balance = None

    initial_balance = float(clean_text_list[-5]
                            .replace(",", "").split(" : ")[1])
    credit_mutation = float(clean_text_list[-4]
                            .replace(",", "").split(" : ")[1].split()[0])
    credit_count = int(clean_text_list[-4].split(" : ")[1].split()[1])
    debit_mutation = float(clean_text_list[-3]
                           .replace(",", "").split(" : ")[1].split()[0])
    debit_count = int(clean_text_list[-3].split(" : ")[1].split()[1])
    final_balance = float(clean_text_list[-2].replace(",", "").split(" : ")[1])

    summary = dict(initial_balance=initial_balance,
                   credit_mutation=credit_mutation,
                   credit_count=credit_count,
                   debit_mutation=debit_mutation,
                   debit_count=debit_count,
                   final_balance=final_balance)
    return summary


def is_first_line_transaction(text_line):
    """
        Pattern for each first line transaction
        started with date with format: dd/mm
    """
    first_splitted = text_line.split()[0]
    if len(first_splitted) == 5 and first_splitted[2] == "/":
        return True
    return False


def is_money_format(input_str):
    if "," in input_str or "." in input_str:
        if input_str.replace(",", "").replace(".", "").isdigit():
            return True
    return False


def get_transaction_details(clean_text_list):
    """
        first we get the starting index for transaction details which start
        from string "TANGGAL KETERANGAN CBG MUTASI SALDO"
        we omit the next line since it always "SALDO AWAL" information
        and get all element until index -5, since -5 to -1
        would be lines for transaction summary

        If a line is first line of a transaction:

            then
                we split the current line

                    1. get transaction_date from first element

                    2. get first element with money format from
                       current splitted line. this should be on mutation column

                    3. transaction_description should be all
                       elements after transaction_date (step 1) and before
                        mutation (step 2)

                    4. if the next element after step 2 contains "DB",
                       then the transaction_type is DEBIT
                        else
                            if no other element after step 2
                                or the next element is money format,
                            then the transaction_type is CREDIT

        else

            if a line is not first line of a transaction,
                then the current line is additional
                description from previous transaction,
            then we add this line to last element's transaction_description
    """
    print('print krna ha ye')
    req = []
    #print(clean_text_list)
    list1 = ['shall be able to','user must','user shall','must do','system shall','allows the user']
    #print(any("18" in clean_text_list))
    
    for dado in clean_text_list:
        #for da in dado:
        
        #if('shall be able to' in dado):
        for ded in list1:
            if(ded in dado):
                req.append(dado)

            #print(dado)
        #print(dado)


    print(req)
    
    #start_idx = clean_text_list.index("shall be able to")
    #raw_transaction_list = clean_text_list[start_idx + 2:-5]

    # for raw in raw_transaction_list:
    #     print(raw)

    # transaction_data_list = []

    # for text in raw_transaction_list:
    #     transaction_date = None
    #     transaction_description = None
    #     mutation = None
    #     transaction_type = None  # either DEBIT or CREDIT

    #     if is_first_line_transaction(text):
    #         current_splitted_text = text.split()

    #         transaction_date = current_splitted_text[0]

    #         for idx, el in enumerate(current_splitted_text):
    #             if is_money_format(el):
    #                 mutation = float(el.replace(",", ""))
    #                 transaction_description = " ".join(
    #                                             current_splitted_text[1:idx])
    #                 break

    #         try:
    #             if current_splitted_text[idx+1] == "DB":
    #                 transaction_type = "DEBIT"
    #             elif is_money_format(current_splitted_text[idx+1]):
    #                 transaction_type = "CREDIT"
    #         except IndexError:
    #             transaction_type = "CREDIT"

    #         current_line_data = dict(transaction_date=transaction_date,
    #                                  transaction_description=transaction_description,
    #                                  mutation=mutation,
    #                                  transaction_type=transaction_type)
    #         transaction_data_list.append(current_line_data)
    #     else:
    #         transaction_data_list[-1]["transaction_description"] += (" " + text)

    return req


def main():
    file = "srs6"
    filename = "./data/"+file+".pdf"  # change this to target document
    raw_text = get_raw_text(filename)
    clean_text_list = get_clean_text_list(raw_text)

    #bank_account_data = get_bank_account_data(clean_text_list)
    #transaction_summary = get_transaction_summary(clean_text_list)
    transaction_details = get_transaction_details(clean_text_list)

    df = pd.DataFrame(transaction_details)
  
    df.to_csv("./exported/"+file+".csv", index=False)


if __name__ == '__main__':
    main()
