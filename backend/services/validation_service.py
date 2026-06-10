import pandas as pd


def validate_dataframe(df):

    errors = []
    valid_rows = 0
    invalid_rows = 0

    duplicate_ids = df["record_id"].duplicated()

    for index, row in df.iterrows():

        row_errors = []

        # record_id boş mu
        if str(row["record_id"]).strip() == "":
            row_errors.append(
                {
                    "field_name": "record_id",
                    "error_type": "MISSING_VALUE",
                    "error_message": "record_id boş",
                    "action": "REJECT"
                }
            )

        # Duplicate record_id kontrolü
        if duplicate_ids.iloc[index]:
            row_errors.append(
                {
                    "field_name": "record_id",
                    "error_type": "DUPLICATE_RECORD",
                    "error_message": "Duplicate record_id",
                    "action": "REJECT"
                }
            )

        # Tarih boş mu
        if str(row["Tarih"]).strip() == "":
            row_errors.append(
                {
                    "field_name": "Tarih",
                    "error_type": "MISSING_VALUE",
                    "error_message": "Tarih boş",
                    "action": "REJECT"
                }
            )

        # OEE kontrolü
        if row["OEE"] < 0 or row["OEE"] > 100:
            row_errors.append(
                {
                    "field_name": "OEE",
                    "error_type": "INVALID_RANGE",
                    "error_message": "Geçersiz OEE değeri",
                    "action": "REJECT"
                }
            )

        # Üretilen miktar negatif mi
        if row["Üretilen Miktar"] < 0:
            row_errors.append(
                {
                    "field_name": "Üretilen Miktar",
                    "error_type": "NEGATIVE_VALUE",
                    "error_message": "Üretilen Miktar negatif",
                    "action": "REJECT"
                }
            )

        # Hatalı miktar üretilenden büyük mü
        if row["Hatal? Üretilen Miktar"] > row["Üretilen Miktar"]:
            row_errors.append(
                {
                    "field_name": "Hatalı Üretilen Miktar",
                    "error_type": "BUSINESS_RULE",
                    "error_message": "Hatalı Üretilen Miktar, Üretilen Miktardan büyük",
                    "action": "REJECT"
                }
            )

        if row_errors:

            invalid_rows += 1

            errors.append(
                {
                    "row": index + 1,
                    "errors": row_errors
                }
            )

        else:
            valid_rows += 1

    return {
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
        "errors": errors
    }