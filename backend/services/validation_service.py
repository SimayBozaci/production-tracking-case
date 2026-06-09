def validate_dataframe(df):

    errors = []
    valid_rows = 0
    invalid_rows = 0

    for index, row in df.iterrows():

        row_errors = []

        # record_id boş mu
        if str(row["record_id"]).strip() == "":
            row_errors.append("record_id boş")

        # Tarih boş mu
        if str(row["Tarih"]).strip() == "":
            row_errors.append("Tarih boş")

        # Üretilen miktar negatif mi
        if row["Üretilen Miktar"] < 0:
            row_errors.append("Üretilen Miktar negatif")

        # Hatalı miktar üretilenden büyük mü
        if row["Hatal? Üretilen Miktar"] > row["Üretilen Miktar"]:
            row_errors.append(
                "Hatalı Üretilen Miktar, Üretilen Miktardan büyük"
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