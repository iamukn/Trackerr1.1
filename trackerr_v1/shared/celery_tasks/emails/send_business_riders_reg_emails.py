from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def send_welcome_email(to, username, account_type, password=''):
    subject = "Welcome to TrackerrGo"

    context = {
        "user_name": username.title(),
        "login_url": "https://trackerrgo.com/login/",
        "android_url": "https://trackerrgo.com/login/",
        "to": to[0],
        "account_type": account_type,
        "password": password
    }

    if account_type.lower() == 'business':
        html_content = render_to_string(
            "emails/business_welcome.html",
            context
        )

        text_content = f"""
        Hello {context["user_name"]},

        Your TrackerrGo {account_type.title()} account has been successfully created.

        Login: {context["login_url"]}

        Thanks,
        The TrackerrGo Team
        """
    elif account_type.lower() == 'logistics':
        html_content = render_to_string(
                "emails/logistics_welcome.html",
                context
        )


        text_content = f"""
        Hello {context["user_name"]},
        Your TrackerrGo Rider account has been successfully created.
        
        Email: {context["to"]}
        Password: {context["password"]}

        Download App: {context["android_url"]}
        Thanks,
        The TrackerrGo Team
        """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_SENDER,
        to=[to[0]],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
