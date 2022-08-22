
# Excel User Defined Functions

A few handy Excel UDFs. 

### Instructions

1. Open Excel, press Alt+F11 to open VBA console.
2. Create a new module and copy the code in Functions to it.
3. Save the Excel file as an "AddIn" i.e. with an .xlam extension
4. Save the file in ../Users/[username]/AppData/Roaming/Microsoft/AddIns

Thats it! It should now appear under Excel AddIns in the Options.

### Reference

**aySumIf(sumRange As Range, colSum As Boolean, colCriteria, colRange As Range, rowCriteria, rowRange As Range)**

Regular excel sumif, does addition across criteria in a column. This takes a criteria from a row and a column and then does the addition. Additionally, it can do addition across columns or rows.

- sumRange = range of values which are to be added. This should have number of rows = rowRange and columns = colRange. It should include only values for addition, no strings, etc.
- colSum = boolean criteria specifying whether addition is to be done over rows or columns. TRUE = column sum.
- colCriteria = criteria to test/match in column range for addition.
- colRange = range to test/match colCriteria. columns should equal columns in sumRange.
- rowCriteria = criteria to test/match in row range for addition.
- rowRange = range to test/match rowCriteria. rows should equal rows in sumRange.

**ayAverageIf(avgRange As Range, colAvg As Boolean, follow As Boolean, colCriteria, colRange As Range, rowCriteria, rowRange As Range)**

Regular excel averageif does average across criteria in a column. This takes a criteria from a column and a row and then does the average. Additionally, it can do average across a columns or rows.

- avgRange = range of values which are to be averaged. This should have number of rows = rowRange and columns = colRange. It should include only values for average, no strings, etc.
- colAvg = boolean criteria specifying whether average is to be done over rows or columns. TRUE = column average.
- follow = boolean criteria specifying whether the dimension of average should follow the other dimension. This can come in use when different criteria applies to each value in the average dimension, e.g. values above or below certain standard deviation in which case each value has to be tested separately. In this case the criteria test/match range of dimension for average would have to *follow* the change in the other range, since a different criteria is being applied to each value.
  - When colAvg = TRUE, follow = TRUE, the colRange should equal the avgRange in both dimensions and vice versa when colAvg = FALSE and follow = TRUE
- colCriteria = criteria to test/match in column range for average.
- colRange = range to test/match colCriteria. (see follow)
- rowCriteria = criteria to test/match in row range for average.
- rowRange = range to test/match rowCriteria. (see follow)

**ayStDevIf(dataRange As Range, criteria, criteriaRange As Range)**

This is equivalent of regular excel sumif for calculating standard deviation.

**aySumIf2(sumRange As Range, colSum As Boolean, colCriteria As Boolean, colRange As Range, rowCriteria, rowRange As Range, specialCriteria, Optional specialRange As Range)**

This is a modified version of aySumIf. it takes an additional specialCriteria as an operator (>, <, =, etc.). This comes in handy when addition is to be done by some numeric criteria, in addition to the row and column criteria. For instance, values greater than some fixed value, or values only occuring in months numbered greater than 9, i.e. October, November and December.

- sumRange = range of values which are to be added. This should have number of rows = rowRange and columns = colRange. It should include only values for addition, no strings, etc.
- colSum = boolean criteria specifying whether addition is to be done over rows or columns. TRUE = column sum.
- colCriteria = criteria to test/match in column range for addition.
- colRange = range to test/match colCriteria. columns should equal columns in sumRange.
- rowCriteria = criteria to test/match in row range for addition.
- rowRange = range to test/match rowCriteria. rows should equal rows in sumRange.
- specialCriteria = special operator criteria expressed as [operator][value], string format.
- specialRange = range to test/match specialCriteria. When colSum = TRUE, this should match the colRange and vice versa. 

**ayRangeRef(inRange As Range, Optional colIncrement As Variant = 0)**

This returns an excel range in string format. This comes in use when automating sheets with macros. Then range of values can be stored in specific cells and that reference can be passed to the macro, instead of updating the range in the macro itself.

- inRange = range for which string format reference is required.
- colIncrement = optional criteria to specify if existing string format range reference should increment by column reference.


