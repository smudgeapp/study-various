


Function aySumIf(sumRange As Range, colSum, colCriteria, colRange As Range, rowCriteria, rowRange As Range)

Dim sumFinalVal As Variant
sumFinalVal = 0

If colSum = True Then

Dim rowKey As Integer
Dim colKeys() As Integer
Dim colKeyLen As Integer
colKeyLen = 0

For i = 1 To rowRange.Rows.count
Dim chkVal
chkVal = rowRange.Cells(i, 1)
If chkVal = rowCriteria Then
rowKey = i
Exit For
End If
Next i

Dim chkVal2 As Variant

For j = 1 To colRange.Columns.count
chkVal2 = colRange.Cells(1, j)


If chkVal2 = colCriteria Then
ReDim Preserve colKeys(colKeyLen)
colKeys(colKeyLen) = j
colKeyLen = colKeyLen + 1
End If

Next j


For k = 0 To UBound(colKeys)
sumFinalVal = sumFinalVal + sumRange(rowKey, colKeys(k))
Next k


Else

Dim colKey As Integer
Dim rowKeys() As Integer
Dim rowKeyLen As Integer
rowKeyLen = 0

For i = 1 To colRange.Columns.count
Dim chkVal3
chkVal3 = colRange.Cells(1, i)
If chkVal3 = colCriteria Then
colKey = i
Exit For
End If
Next i

For j = 1 To rowRange.Rows.count
Dim chkVal4
chkVal4 = rowRange(j, 1)
If chkVal4 = rowCriteria Then
ReDim Preserve rowKeys(rowKeyLen)
rowKeys(rowKeyLen) = j
rowKeyLen = rowKeyLen + 1
End If
Next j

For k = 0 To UBound(rowKeys)
sumFinalVal = sumFinalVal + sumRange(rowKeys(k), colKey)
Next k


End If

aySumIf = sumFinalVal

End Function




Function ayAverageIf(avgRange As Range, colAvg, follow, colCriteria, colRange As Range, rowCriteria, rowRange As Range)

Dim avgValSum As Variant
avgValSum = 0
Dim avgArrLen As Integer
avgArrLen = 0
Dim avgFinalVal As Variant



If colAvg = True Then

Dim rowKey As Integer
Dim colKeys() As Integer
Dim colKeyLen As Integer
colKeyLen = 0

For i = 1 To rowRange.Rows.count
Dim chkVal
chkVal = rowRange.Cells(i, 1)
If chkVal = rowCriteria Then
rowKey = i
Exit For
End If
Next i

Dim chkVal2 As Variant

For j = 1 To colRange.Columns.count
chkVal2 = colRange.Cells(1, j)
If follow = True Then
chkVal2 = colRange.Cells(rowKey, j)
End If

If chkVal2 = colCriteria Then
ReDim Preserve colKeys(colKeyLen)
colKeys(colKeyLen) = j
colKeyLen = colKeyLen + 1
End If

Next j


For k = 0 To UBound(colKeys)
avgValSum = avgValSum + avgRange(rowKey, colKeys(k))
Next k


avgArrLen = UBound(colKeys) - LBound(colKeys) + 1

avgFinalVal = avgValSum / avgArrLen


Else

Dim colKey As Integer
Dim rowKeys() As Integer
Dim rowKeyLen As Integer
rowKeyLen = 0

For i = 1 To colRange.Columns.count
Dim chkVal3
chkVal3 = colRange.Cells(1, i)
If chkVal3 = colCriteria Then
colKey = i
Exit For
End If
Next i

For j = 1 To rowRange.Rows.count
Dim chkVal4
chkVal4 = rowRange.Cells(j, 1)
If follow = True Then
chkVal4 = rowRange.Celss(j, colKey)
End If

If chkVal4 = rowCriteria Then
ReDim Preserve rowKeys(rowKeyLen)
rowKeys(rowKeyLen) = j
rowKeyLen = rowKeyLen + 1
End If
Next j

For k = 0 To UBound(rowKeys)
avgValSum = avgValSum + avgRange(rowKeys(k), colKey)
Next k

avgArrLen = UBound(rowKeys) - LBound(rowKeys) + 1
avgFinalVal = avgValSum / avgArrLen

End If

ayAverageIf = avgFinalVal

End Function



Function ayStDevIf(dataRange As Range, criteria, criteriaRange As Range)

Dim dataCount
dataCount = 0
Dim avgSum
avgSum = 0
Dim dataVals()

Dim rangeCount
rangeCount = dataRange.Rows.count

For i = 1 To rangeCount
If criteria = criteriaRange(i, 1).Value Then
If IsNumeric(dataRange(i, 1).Value) = True Then
dataCount = dataCount + 1
ReDim Preserve dataVals(dataCount)
dataVals(dataCount - 1) = dataRange(i, 1).Value
avgSum = avgSum + dataVals(dataCount - 1)
End If
End If
Next i

Dim avgVal
avgVal = avgSum / dataCount
Dim sumSqDiff As Double
sumSqDiff = 0
Dim calcCount
calcCount = dataCount - 1


For j = 0 To calcCount
Dim avgDiff
avgDiff = dataVals(j) - avgVal
Dim sqDiff As Double
sqDiff = (dataVals(j) - avgVal) ^ 2
sumSqDiff = sumSqDiff + sqDiff
Next j


Dim stDevVal As Double
stDevVal = sumSqDiff / dataCount
Dim stDev
stDev = Sqr(stDevVal)

ayStDevIf = stDev

End Function

Function aySumIf2(sumRange As Range, colSum, colCriteria, colRange As Range, rowCriteria, rowRange As Range, specialCriteria, Optional specialRange As Range)

Dim sumFinalVal
sumFinalVal = 0


If colSum = True Then


Dim rowKey As Integer
Dim colKeys() As Integer
Dim colKeyLen As Integer
colKeyLen = 0

For i = 1 To rowRange.Rows.count
Dim chkVal
chkVal = rowRange.Cells(i, 1)
If chkVal = rowCriteria Then
    rowKey = i
    Exit For
End If

Next i


Dim chkVal2 As Variant

For j = 1 To colRange.Columns.count
chkVal2 = colRange.Cells(1, j)
If chkVal2 = colCriteria Then
    If specialCriteria <> "Nil" Then
        Dim condStr
        condStr = specialRange.Cells(1, j).Value & specialCriteria
        If Evaluate(condStr) Then
            ReDim Preserve colKeys(colKeyLen)
            colKeys(colKeyLen) = j
            colKeyLen = colKeyLen + 1
        End If
    Else
        colKeys(colKeyLen) = j
        colKeyLen = colKeyLen + 1
    End If
End If

Next j


For k = 0 To UBound(colKeys)
sumFinalVal = sumFinalVal + sumRange(rowKey, colKeys(k))
Next k

Else

Dim colKey As Integer
Dim rowKeys() As Integer
Dim rowKeyLen As Integer
rowKeyLen = 0


For i = 1 To colRange.Columns.count
Dim chkVal3
chkVal3 = colRange.Cells(1, i)
If chkVal3 = colCriteria Then
    colKey = i
    Exit For
End If
Next i

For j = 1 To rowRange.Rows.count
Dim chkVal4
chkVal4 = rowRange(j, 1)

If chkVal4 = rowCriteria Then
    ReDim Preserve rowKeys(rowKeyLen)
    If specialCriteria <> "Nil" Then
        Dim condStr2
        condStr2 = specialRange.Cells(j, 1).Value & specialCriteria
        If Evaluate(condStr2) Then
            rowKeys(rowKeyLen) = j
            rowKeyLen = rowKeyLen + 1
        End If
    Else
        rowKeys(rowKeyLen) = j
        rowKeyLen = rowKeyLen + 1
    End If
End If

Next j

For k = 0 To UBound(rowKeys) - 1
sumFinalVal = sumFinalVal + sumRange(rowKeys(k), colKey)
Next k

End If


aySumIf2 = sumFinalVal

End Function




Function ayRangeRef(inRange As Range, Optional colIncrement As Variant = 0)

Dim beginCell
Dim rowCount
Dim colCount
Dim outAdd
Dim beginAdd
Dim endAdd
Dim endCell

Debug.Print colIncrement

If colIncrement = 0 Then
    rowCount = inRange.Rows.count
    colCount = inRange.Columns.count
    Set beginCell = inRange.Cells(1, 1)
    Set endCell = inRange.Cells(rowCount, colCount)
    
Else
    Dim rangeStr
    rangeStr = inRange.Cells(1, 1).Value
    Debug.Print rangeStr
    Set convRange = Range(rangeStr)
    rowCount = convRange.Rows.count
    colCount = convRange.Columns.count
    If colIncrement = 1 Then
        Set beginCell = convRange.Cells(1, 2)
        Set endCell = convRange.Cells(rowCount, colCount + 1)
    ElseIf colIncrement = 2 Then
        Set beginCell = convRange.Cells(2, 1)
        Set endCell = convRange.Cells(rowCount + 1, colCount)
    End If
End If


beginAdd = beginCell.Address(RowAbsolute:=False, ColumnAbsolute:=False)
Debug.Print beginAdd
endAdd = endCell.Address(RowAbsolute:=False, ColumnAbsolute:=False)
outAdd = beginAdd & ":" & endAdd


ayRangeRef = outAdd



End Function
