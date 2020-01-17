from datetime import datetime

import mysql.connector
import xlsxwriter

mydb = mysql.connector.connect(
    database="envolsadora",
    host="localhost",
    user="root",
    passwd="tecnomotor"
)

mycursor = mydb.cursor()

now = datetime.now()
date = now.strftime("%m-%Y")
# Create a workbook and add a worksheet.
nombre = str('Reporte_mensual_'+str(date)+'.xlsx')
print(nombre)
workbook = xlsxwriter.Workbook(nombre)
worksheet = workbook.add_worksheet()

mycursor.execute("select id,round(sum(pesaje),2),date_format(date,'%d-%m') from pesajes p where month(p.date) = month(now()) and year(p.date) = year(now()) group by day(p.date)")
result = mycursor.fetchall()
print(result)
input('asd')
expenses = result
# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0
# Iterate over the data and write it out row by row.
worksheet.write(row, col, "Peso")
worksheet.write(row, col + 1, "Fecha")
row +=1
for id, peso, fecha in (expenses):
    worksheet.write(row, col, peso)
    worksheet.write(row, col + 1,str(fecha))
    row += 1


workbook.close()
