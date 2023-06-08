# custom_action.py
from datahub_actions.action.action import Action
from datahub_actions.event.event_envelope import EventEnvelope
from datahub_actions.pipeline.pipeline_context import PipelineContext
import smtplib



class CustomAction(Action):
    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext) -> "Action":
        # Simply print the config_dict.
        print(config_dict)
        return cls(ctx)

    def __init__(self, ctx: PipelineContext):
        self.ctx = ctx

    def act(self, event: EventEnvelope) -> None:
        # Do something super important.
        # For now, just print. :) 

        # данные почтового сервиса
        user = "postmaster@astera.in"
        passwd = """nejgumssvpohsszx"""
        server = "smtp.yandex.ru"
        port = 587
        # тема письма
        subject = "Метаданные изменились!"

        # кому
        to = "{{ notification_mail }}"

        # кодировка письма
        charset = 'Content-Type: text/html; charset=utf-8'
        mime = 'MIME-Version: 1.0'
        # текст письма
        #text = f"Категория: {event.event.category}\nТип объекта: {event.event.entityType}\nИдентификаторов ресурса - {event.event.entityUrn}\nОперация - {event.event.operation}\nМодификатор - {event.event.modifier}\nПараметры - {event.event.parameters}\nПользователь - {event.event.auditStamp.actor}"
        text = """
<html>
<head>

   <title>Tutsplus Email Newsletter</title>
   <link rel="stylesheet" href="css.css">
</head>
<body>
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>

<table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
    <tr>
      <td>
        <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
          <tr>
            <td width="570" align="center"  bgcolor="#d80a3e"><h1>Метаданные изменились!</h1></td>
          </tr>
        </table>
      </td>
    </tr>
    
    <tr>
      <td>
        <table id="content-4" cellpadding="20" cellspacing="0" align="center">
          <tr>
            <td >Категория</td>

            <td>{category}</td>
          </tr>
          <tr>
            <td>Тип объекта</td>
            <td>{entityType}</td>
          </tr>
          <tr>
            <td>Идентификаторов ресурса</td>
            <td>{entityUrn}</td>
          </tr>
          <tr>
            <td>Операция</td>
            <td>{operation}</td>
          </tr>
          <tr>
            <td>Модификатор</td>
            <td>{modifier}</td>
          </tr>
          <tr>
            <td>Параметры</td>
            <td>{parameters}</td>
          </tr>
          <tr>
            <td>Пользователь</td>
            <td>{actor}</td>
          </tr>
        </table>
      </td>
    </tr>
  </table>

</td></tr></table><!-- wrapper -->
</body>
</html>

"""
        # формируем тело письма
        body = "\r\n".join((f"From: {user}", f"To: {to}", 
               f"Subject: {subject}", mime, charset, "", text.format(category = event.event.category, entityType = event.event.entityType, entityUrn = event.event.entityUrn, operation= event.event.operation, modifier = event.event.modifier, parameters = event.event.parameters, actor = event.event.auditStamp.actor)))

        try:
            # подключаемся к почтовому сервису
            smtp = smtplib.SMTP(server, port)
            smtp.starttls()
            smtp.ehlo()
            # логинимся на почтовом сервере
            smtp.login(user, passwd)
            # пробуем послать письмо
            smtp.sendmail(user, to, body.encode('utf-8'))
        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
        finally:
            smtp.quit()

    def close(self) -> None:
        pass
