def SendEmail(recipients, sender, subject, body, attachments = None):
	u"""\
	Send email.
	recipients = ('post@example.com', 'another@example.com')
	"""

	# Import smtplib for the actual sending function
	import smtplib

	# Import the email modules we'll need
	from email.mime.text import MIMEText

	msg = MIMEText(body)

	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ','.join(recipients)

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail(sender, recipients, msg.as_string())
	s.quit()
