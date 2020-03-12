import datetime
import os.path
from csv import writer
from csv import DictWriter
 
def append_list_as_row(file_name, list_of_elem):

    if (os.path.exists(file_name))==False:
        with open(file_name, 'w', newline='') as file:
            writers = writer(file)
            # writers.writerows(["Fecha","Hora","Evento Negativo","Evento Positivo"])
            writers.writerow(["Fecha", "Hora", "Tipo Evento", "Duracion", "frame"])


    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)




def main(evento,tiempo,frame):
    
    currentDT = datetime.datetime.now()
    name='Reporte_{}-{}-{}.csv'.format(currentDT.year,currentDT.month,currentDT.day)
    # List of strings
    row_contents = ['{}/{}/{}'.format(currentDT.year,currentDT.month,currentDT.day),
                    '{}:{}:{}'.format(currentDT.hour,currentDT.minute,currentDT.second),
                    evento,
                    str(tiempo)+" seg",
                    frame]
 
    # Append a list as new line to an old csv file
    append_list_as_row(name, row_contents)

 
 