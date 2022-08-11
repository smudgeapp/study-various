# EXCEL USER-DEFINED FUNCTIONS

Some handy functions for MS Excel.

### INSTRUCTIONS

1. Open excel and press Alt+F11 to open VBA console.
2. Copy this code into a new blank module.
3. Then save the file as 'ExcelAddIn' with extension '.xlam'.
4. Copy the .xlam extension file into ../AppData/Microsoft/AddIns - (path may vary depending on excel version/windows version/general local machine setup).

### REFERENCE

1. **aySumIf(sumRange As Range, colSum As Boolean, colCriteria, colRange As Range, rowCriteria, rowRange As Range)**

Regular sumif, takes criteria from a single column, this method takes a criteria from a column and a row to match values. 

For multiple criteria (sumifs equivalent) in column or rows, convenience method is to concatenate the criteria into a single string/cell and then apply the formula for the unique values.

- sumRange = range of values to be added. Range columns should match the number of columns in the colRange and rows should match the rows in the rowRange
- colSum = criteria determining whether addition is to be done over rows or columns. TRUE = sum columns
- colCriteria = criteria for addition in columns.
- colRange = column range to search for criteria.
- rowCriteria = criteria for addition in rows.
- rowRange = row range to search for criteria.

2. **ayAverageIf(averageRange As Range, [to be continued....]**

3. **ayStDevIf(dataRange As Range, criteria, criteriaRange As Range)**

Equivalent of basic excel sumif function for calculating standard deviation.

- dataRange = range of values for which standard deviation is to be calculated
- criteria = criteria of the values to be selected
- criteriaRange = range of criteria values.

4. **ayRangeRef(rangeRef As Range, Optional colIncrement as Variant = 0)**

It outputs the excel format range reference as a string. This can be used to provide a single cell reference to various automation macros. Rather than having to modify the range in the macro itself, only update the range in the referenced cell.

- rangeRef = range for which range string is required
- colIncrement = optional value defaults to 0. When this value is specified, the output column will be incremented by the column value of the specified range passed as rangeRef.

5. **aySumIf2(sumRange As Range, colSum, colCriteria, colRange As Range, rowCriteria, rowRange As Range, specialCriteria, Optional specialRange As Range)**

Modified aySumIf to take additional criteria string with an operator. Originally, it was written to sum monthly financial data. The special criteria would specify the operator (>, <, =, >=, <=) along with the number of month. For instance, ">=9" would only sum values for months with serial number greater than and equal to 9. This was helpful in obtaining sums of, for instance, different forecast scenarios for the same period, upto a specific number of months.

Depending on the nature of data this could be applied to any other kind of dataset.

- sumRange = range of values to be added. Range columns should match the number of columns in the colRange and rows should match the rows in the rowRange
- colSum = boolean value to specify whether to sum values in columns or rows. TRUE = column sums
- colCriteria = criteria for addition in columns.
- colRange = column range to search for criteria.
- rowCriteria = criteria for addition in rows.
- rowRange = row range to search for criteria.
- specialCriteria = equality criteria (>, <, =, >=, <=) specific value as a string. ">=9", "<=3".
- specialRange = range of values to match the special criteria.
