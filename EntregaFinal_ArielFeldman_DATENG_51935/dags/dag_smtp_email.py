from datetime import datetime,timedelta
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_env = Variable.get('var_smtp', deserialize_json=True)
_pass=Variable.get('SMTP_PASSWORD')

error_message_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Error de valor de dato</title>
</head>
<body>
  <h1>Error de valor de dato</h1>
  <p>Se ha producido un error al procesar los datos. El valor del dato no es válido.</p>
  <p>Por favor, revisa los datos y asegúrate de que todos los valores sean correctos.</p>
  <p>Si necesitas ayuda, no dudes en contactarnos.</p>
</body>
</html>
"""

def enviar():
    try:
        x=smtplib.SMTP('smtp.gmail.com',int(smtp_env['PORT']))
        x.starttls()
        x.login(smtp_env['EMAIL'],_pass)

        # Crear el objeto del mensaje y establecer los datos del encabezado
        message = MIMEMultipart('alternative')
        message['From'] = smtp_env['EMAIL']
        message['To'] = smtp_env['EMAIL']
        message['Subject'] = 'Ganaste un premio'

        # Agregar el contenido del mensaje en formato HTML
        message.attach(MIMEText(error_message_html, 'html'))

        x.sendmail(
            from_addr=smtp_env['EMAIL'],
            to_addrs='arielmfeldman.af@gmail.com',
            msg=message.as_string(),
        )
        print('Exito')
    except Exception as exception:
        print(exception)
        print('Failure')

# Establecer argumentos por default
default_args={
    'owner':'Ariel Feldman',
    'depend_on_past':False,
    'retries':10, 
    'retry_delay':timedelta(seconds=30),
    'email':['arielmfeldman.af@gmail.com'], #
    'email_on_retry':['arielmfeldman.af@gmail.com'], #
    'email_on_failure':['arielmfeldman.af@gmail.com'], #
}

with DAG(
    dag_id='dag_smtp_email_automatico',
    description='envio de email automatico',
    start_date=datetime(2023,7,31,21,2),
    default_args=default_args,
    schedule_interval=timedelta(seconds=30),
    tags=['envio_mail'],
    catchup=False
) as dag:

    tarea_1=PythonOperator(
        task_id='dag_envio',
        python_callable=enviar
    )

    tarea_1