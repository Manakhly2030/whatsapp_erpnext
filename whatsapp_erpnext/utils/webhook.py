"""Webhook."""
import frappe
import json
import requests
import time
from frappe.utils import get_site_name
from werkzeug.wrappers import Response
import frappe.utils
from datetime import datetime
import pytz
from frappe.utils import cint

settings = frappe.get_doc(
			"WhatsApp Settings", "WhatsApp Settings",
		)
token = settings.get_password("token")
url = f"{settings.url}/{settings.version}/"
bench_location = frappe.utils.get_bench_path()
site_name = get_site_name(frappe.local.request.host)

@frappe.whitelist(allow_guest=True)
def webhook():
	"""Meta webhook."""
	if frappe.request.method == "GET":
		return get()
	return post()


def get():
	"""Get."""
	hub_challenge = frappe.form_dict.get("hub.challenge")
	webhook_verify_token = frappe.db.get_single_value(
		"Whatsapp Settings", "webhook_verify_token"
	)

	if frappe.form_dict.get("hub.verify_token") != webhook_verify_token:
		frappe.throw("Verify token does not match")

	return Response(hub_challenge, status=200)

def post():
	"""Post."""
	data = frappe.local.form_dict

	# frappe.log_error(message=str(data), title="Webhook Data")

	if data:
		frappe.get_doc({
			"doctype": "Integration Request",
			"template": "Webhook",
			"meta_data": json.dumps(data)
		}).insert(ignore_permissions=True)

	messages = []
	try:
		messages = data["entry"][0]["changes"][0]["value"].get("messages", [])
	except KeyError:
		messages = data["entry"]["changes"][0]["value"].get("messages", [])

	if messages:
		for message in messages:
			contact_no = message.get('from')
			if contact_no:
					short_contact_no = contact_no[-10:]
					contact_query = f"""
					SELECT 
                        c.name, 
                        dl.link_doctype, 
                        dl.link_name 
                    FROM 
                        `tabContact` AS c 
                    JOIN 
                        `tabContact Phone` AS cp 
                        ON cp.parent = c.name 
                    JOIN 
                        `tabDynamic Link` AS dl 
                        ON dl.parent = c.name 
                    WHERE 
                        LENGTH(cp.phone) >= 10
                        AND (cp.phone = '{contact_no}' OR cp.phone LIKE '%{short_contact_no}')
                    ORDER BY 
                        CASE dl.link_doctype
                            WHEN 'Customer' THEN 1
                            WHEN 'Lead' THEN 2
                            ELSE 3
                        END,
                        c.modified DESC
                    LIMIT 1;
				"""

			contact_details = frappe.db.sql(contact_query, as_dict=True)

			link_to = ""
			link_name = ""
			contact_name = ""
			if contact_details:
				contact = contact_details[0]
				link_to = contact.get("link_doctype", "")
				link_name = contact.get("link_name", "")
				contact_name = contact.get("name", "")
			# else:
				# Log if no contact is found
				# frappe.log_error(message=f"No contact found for phone number: {contact_no}", title="Contact Not Found")
			message_type = message['type']
			messaage_datetime = datetime.fromtimestamp(cint(message['timestamp']))
			
			if message_type == 'text':
				frappe.get_doc({
					"doctype": "WhatsApp Message",
					"type": "Incoming",
					"from": message['from'],
					"message_datetime": messaage_datetime,
					"date": messaage_datetime.date(),
					"link_to": link_to,
					"link_name": link_name,
					"contact": contact_name,
					"message": message['text']['body'],
					"message_id": message['id'],
					"content_type":message_type,
					"status": "Received"
				}).insert(ignore_permissions=True)
			
			elif message_type in ["image", "audio", "video", "document"]:
				media_id = message[message_type]["id"]
				headers = {
					'Authorization': 'Bearer ' + token
				}
				response = requests.get(f'{url}{media_id}/', headers=headers)

				if response.status_code == 200:
					media_data = response.json()
					media_url = media_data.get("url")
					mime_type = media_data.get("mime_type")
					file_extension = mime_type.split('/')[1]

					media_response = requests.get(media_url, headers=headers)
					if media_response.status_code == 200:
						file_data = media_response.content
						time.sleep(1)

						whatsapp_message_doc = frappe.get_doc({
							"doctype": "WhatsApp Message",
							"type": "Incoming",
							"from": message['from'],
							"message_datetime": messaage_datetime,
							"date": messaage_datetime.date(),
							"link_to": link_to,
							"link_name": link_name,
							"contact": contact_name,
							"message_id": message['id'],
							"file_name": message['document']['filename'],
							# "message": f"/files/{file_name}",
							# "attach" : f"/files/{file_name}",
							"content_type": message_type,
							"status": "Received"
						}).insert(ignore_permissions=True)

						file_doc = frappe.get_doc(
							{
								"doctype": "File",
								"attached_to_doctype": "WhatsApp Message",
								"attached_to_name": whatsapp_message_doc.name,
								"attached_to_field": "attach",
								"file_name": message['document']['filename'],
								"is_private": cint(1),
								"content": file_data,
							}
						).save(ignore_permissions=True)

						whatsapp_message_doc.db_set("attach", file_doc.file_url, update_modified=False)
						whatsapp_message_doc.db_set("message", file_doc.file_url, update_modified=False)

	else:
		changes = None
		try:
			changes = data["entry"][0]["changes"][0]
		except KeyError:
			changes = data["entry"]["changes"][0]
		update_status(changes)
	return


def update_status(data):
	"""Update status hook."""
	if data.get("field") == "message_template_status_update":
		update_template_status(data['value'])

	elif data.get("field") == "messages":
		update_message_status(data['value'])


def update_template_status(data):
	"""Update template status."""
	frappe.db.sql(
		"""UPDATE `tabWhatsApp Templates`
		SET status = %(event)s
		WHERE id = %(message_template_id)s""",
		data
	)



def update_message_status(data):
	"""Update message status."""
	id = data['statuses'][0]['id']
	status = data['statuses'][0]['status']
	conversation = data['statuses'][0].get('conversation', {}).get('id')
	name = frappe.db.get_value("WhatsApp Message", filters={"message_id": id})

	doc = frappe.get_doc("WhatsApp Message", name)
	if doc.type != "Incoming":
		doc.status = status.title()
	if conversation:
		doc.conversation_id = conversation
	doc.save(ignore_permissions=True)