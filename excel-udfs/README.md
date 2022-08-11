# EXCEL USER-DEFINED FUNCTIONS

Some handy functions for MS Excel.

### INSTRUCTIONS

1. Open excel and press Alt+F11 to open VBA console.
2. Copy this code into a new blank module.
3. Then save the file as .xlam.
4. Copy the .xlam file into ../AppData/Microsoft/AddIns - (path may vary depending on excel version/windows version/general local machine setup).

### REFERENCE

1. aySumIf(sumRange As Range, colSum As Boolean, colCriteria, colRange As Range, rowCriteria, rowRange As Range)

Regular sumif, takes criteria from a single column, this method takes a criteria from a column and a row to match values. 

For multiple criterias (sumifs) in column or rows, convenience method is to concatenate the criteria into a single string/cell and then apply the formula for the unique values.

sumRange = range of values to be added
colSum = criteria determining whether addition is to be done over rows or columns. TRUE = sum columns
colCriteria = criteria for addition in columns.
colRange = column range to search for criteria.
rowCriteria = criteria for addition in rows.
rowRange = row range to search for criteria.

2. ayAverageIf(averageRange As Range, [to be continued....]
