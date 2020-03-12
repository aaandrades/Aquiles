import matplotlib.pyplot as plt
import csv
import datetime


currentDT = datetime.datetime.now()


nombre='Reporte_{}-{}-{}.csv'.format(currentDT.year,currentDT.month,currentDT.day)
with open(nombre, mode='r') as csv_file:
    phone=0
    handphone=0
    laptop=0
    cup=0

    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'{" || ".join(row)}')
            line_count += 1
        
        if f'{row["Tipo Evento"]}'=='Hablando por Celular':
            phone+=1
        elif f'{row["Tipo Evento"]}'=='Usando Celular':
            handphone+=1
        elif f'{row["Tipo Evento"]}'=='Sujetando Laptop':
            laptop+=1
        elif f'{row["Tipo Evento"]}'=='Sosteniendo Vaso':
            cup+=1
        
        # print(f'{row["Fecha"]} || {row["Hora"]} || {row["Evento Negativo"]} || {row["Evento Positivo"]} || {row["Causa"]}') PRINT FORMAT
        line_count += 1
    print("\n")
    print(f'Total de Eventos reportados: {line_count-1}')
    print(f'\t Hablando por Celular: {phone}')
    print(f'\t Usando Celular: {handphone}')
    print(f'\t Sosteniendo Laptop: {laptop}')
    print(f'\t Sosteniendo vaso: {cup}')


# Data to plot
labels = 'Hablando por Celular', 'Usando Celular', 'Sosteniendo Laptop', 'Sosteniendo Vaso'
sizes = [phone, handphone, laptop, cup]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

# Plot
patches=plt.pie(sizes, autopct='%1.1f%%',  startangle=140)


# patches, texts = plt.pie(sizes, colors=colors,shadow=True, startangle=90)
plt.title('Estadísticas Módulo Escaleras \n{}/{}/{}'.format(currentDT.year,currentDT.month,currentDT.day), fontdict=None, loc='center', pad=None)
plt.legend(labels, loc="best")

plt.axis('equal')
plt.tight_layout()
plt.show()