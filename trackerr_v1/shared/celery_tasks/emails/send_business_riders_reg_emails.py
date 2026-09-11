from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(to, username, account_type, password=''):
    subject = "Welcome to Trackerr"

    context = {
        "user_name": username.title(),
        "login_url": "https://trackerr.africa/login/",
        "android_url": "https://trackerr.africa/login/",
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

        Your Trackerr {account_type.title()} account has been successfully created.

        Login: {context["login_url"]}

        Thanks,
        The Trackerr Team
        """
    elif account_type.lower() == 'logistics':
        html_content = render_to_string(
                "emails/logistics_welcome.html",
                context
        )


        text_content = f"""
        Hello {context["user_name"]},
        Your Trackerr Rider account has been successfully created.
        
        Email: {context["to"]}
        Password: {context["password"]}

        Download App: {context["android_url"]}
        Thanks,
        The Trackerr Team
        """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email="Trackerr <noreply@trackerr.africa>",
        to=[to[0]],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
