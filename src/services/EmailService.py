import os

from smtplib import SMTP_SSL
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

class UseEmailService:
   def createMailTemplate(self, mailData):
      return f"""
      <table align="center" style="width: 100%; max-width: 500px; padding: 30px 20px; border: 1px solid #c5c5c5; border-radius: 10px;">
         <tbody style="text-align: center; color: #646369; font-size: 20px;">
            <tr>
               <td style="font: 700 35px sans-serif; color: #0066FF; padding-bottom: 15px;">
                  Good Notes
               </td>
            </tr>
            <tr>
               <td>
                  Olá, <b>{mailData['name']}</b>!
               </td>
            </tr>
            <tr>
               <td>
                  {mailData['title']}
               </td>
            </tr>
            <tr>
               <td style="font-size: 17px; padding-top: 10px;">
                  {mailData['subtitle']}
               </td>
            </tr>
            <tr style="height: 90px;">
               <td>
                  <span style="margin: 25px 0; color: #0066FF; font: 700 25px sans-serif; letter-spacing: 5px; border: 1px solid #c5c5c5; background-color: #E8E8E8; padding: 15px 20px; border-radius: 5px;">
                     {mailData['code']}
                  </span>
               </td>
            </tr>
            <tr>
               <td style="font-size: 12px;">
                  Esse código tem a duração de 15 minutos.
               </td>
            </tr>
            <tr>
               <td style="font-size: 16px; padding-top: 10px;">
                  Por que é preciso confirmar o e-mail?
               </td>
            </tr>
            <tr>
               <td style="font-size: 13px; text-align: justify ;padding: 10px 5px 15px 5px;">
                  Isso é necessário para confirmar que este e-mail pertence à você. O nosso serviço oferece algumas funcionalidades que só podem ser utilizadas através do e-mail, por isso nós filtramos apenas os usuários autênticos.
               </td>
            </tr>
            <tr>
               <td style="font-size: 15px; padding-top: 15px; border-top: 1px solid #c5c5c5; color: #000">
                  Se você não fez essa solicitação, por favor ignore este e-mail.
               </td>
            </tr>
            <tr>
               <td style="font-size: 15px; padding-top: 10px;">
                  Atenciosamente
                  <a style="color: #0066FF;" href="https://good-notes-app.herokuapp.com/">Good Notes.</a>
               </td>
            </tr>
         </tbody>
      </table>
      """

   def createActivationMailData(self, user, code):
      return {
         'to': user.email,
         'name': user.username,
         'code': code,
         'subject': 'Código para Ativar Conta',
         'title': 'Seja bem-vindo ao Good Notes.',
         'subtitle': 'O código para ativar a sua conta é:'
      }

   def createPasswordResetMailData(self, user, code):
      return {
         'to': user.email,
         'name': user.username,
         'code': code,
         'subject': 'Código para Redefinir Senha',
         'title': 'Esqueceu sua senha?',
         'subtitle': 'O código para redefinir sua senha é:'
      }

   def createConfirmationMailData(self, user, code):
      return {
         'to': user.email,
         'name': user.username,
         'code': code,
         'subject': 'Código para Confirmar E-mail',
         'title': 'Confirmar novo E-mail.',
         'subtitle': 'O código para confirmar seu e-mail é:'
      }

   def sendMail(self, mailData):

      msg = EmailMessage()

      msg['Subject'] = f"{mailData['subject']} - Good Notes"
      msg['From'] = "Good Notes"
      msg['To'] = mailData['to']

      mailTemplate = self.createMailTemplate(mailData)

      msg.add_alternative(mailTemplate, subtype='html')

      emailConnection = SMTP_SSL('smtp.gmail.com', 465)

      emailConnection.login(
         os.environ.get('EMAIL_ADDRESS'),
         os.environ.get('EMAIL_PASSWORD')
      )
      
      try:
         emailConnection.send_message(msg)
      finally:
         emailConnection.quit()


EmailService = UseEmailService()