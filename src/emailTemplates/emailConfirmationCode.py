def createEmailConfirmationCodeTemplate(name, code):
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
               Olá, <b>{name}</b>!
            </td>
         </tr>
         <tr>
            <td>
               Seja bem-vindo ao Good Notes.
            </td>
         </tr>
         <tr>
            <td style="font-size: 17px; padding-top: 10px;">
               O código para ativar a sua conta é:
            </td>
         </tr>
         <tr style="height: 90px;">
            <td>
               <span style="margin: 25px 0; color: #0066FF; font: 700 25px sans-serif; letter-spacing: 5px; border: 1px solid #c5c5c5; background-color: #E8E8E8; padding: 15px 20px; border-radius: 5px;">
                  {code}
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
               Por que é preciso ativar a conta?
            </td>
         </tr>
         <tr>
            <td style="font-size: 13px; text-align: justify ;padding: 10px 5px 15px 5px;">
               Isso é necessário para diferenciar um usuário de um <em>spam</em>. O nosso serviço oferece algumas funcionalidades que só podem ser utilizadas através do email, por isso nós filtramos apenas os usuários autênticos.
            </td>
         </tr>
         <tr>
            <td style="font-size: 15px; padding-top: 15px; border-top: 1px solid #c5c5c5; color: #000">
               Se você não se cadastrou, por favor ignore este email.
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