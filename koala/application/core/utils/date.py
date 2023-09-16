class Date:
    @staticmethod
    def replace_month_pt_to_numerical(date_str: str) -> str:
        """Replaces Portuguese month abbreviations with numerical ones in a date string.

        Args:
            date_str: A string containing a date with Portuguese month abbreviations.

        Returns:
            A string containing the date with numerical month order.
        """
        replacement_mapping = {'JAN': '01', 'FEV': '02', 'MAR': '03', 
                               'ABR': '04', 'MAI': '05', 'JUN': '06', 
                               'JUL': '07', 'AGO': '08', 'SET': '09',
                               'OUT': '10', 'NOV': '11', 'DEZ': '12'}
        
        splitted_date = date_str.upper().split()
        month = splitted_date[1]
        month = replacement_mapping.get(month)

        if month is not None:
            return f"{splitted_date[-1]}-{month}-{splitted_date[0]}"

        raise Exception('Not a valid month identifier.')