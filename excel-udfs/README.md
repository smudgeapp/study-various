
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

**ayAverageIf(avgRange As Range, colAvg As Boolean, follow As Boolean, colCriteria, colRange As Range, rowCriteria, rowRange As Range)**

Regular excel averageif does average across criteria in a column. This takes a criteria from a column and a row and then does the average. Additionally, it can do average across a columns or rows.

**ayStDevIf(dataRange As Range, criteria, criteriaRange As Range)**

This is equivalent of regular excel sumif for calculating standard deviation.

**aySumIf2(sumRange As Range, colSum As Boolean, colCriteria As Boolean, colRange As Range, rowCriteria, rowRange As Range, specialCriteria, Optional specialRange As Range)**

This is a modified version of aySumIf. it takes an additional specialCriteria as an operator (>, <, =, etc.). This comes in handy when addition is to be done by some numeric criteria, in addition to the row and column criteria. For instance, values greater than some fixed value, or values only occuring in months numbered greater than 9, i.e. October, November and December.

**ayRangeRef(inRange As Range, Optional colIncrement As Variant = 0)**

This returns an excel range in string format. This comes in use when automating sheets with macros. Then range of values can be stored in specific cells and that reference can be passed to the macro, instead of updating the range in the macro itself.

*The repo got accidentally overwritten. The code was obviously available on local machine but the full reference has to be re-written. Till then ...*
