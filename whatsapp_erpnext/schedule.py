import frappe

def schedule_comments():
    calls = frappe.db.get_list(
        "WhatsApp Message",
        {
            "comment": ('is','not set'),
            # "to":("is",'set'),
            # "from":("is",'set'),
        },
        order_by="message_datetime ASC",
        page_length=100,
    )

    for call in calls:
        doc = frappe.get_doc("WhatsApp Message", call.name)
        # whatsapp_message_url = doc.get_url()
        
        # comment_text = doc.get_comment_text(whatsapp_message_url)
        comment = frappe.get_doc(
            {
                "doctype": "Comment",
                "comment_type": "Comment",
                "reference_doctype": doc.link_to,
                "reference_name": doc.link_name,
                "comment_by": frappe.session.user,
                "subject": doc.type,
                "content": doc.message,
            }
        )
        
        comment.save()
        frappe.db.set_value('Comment',comment.name, 'creation', doc.message_datetime)
        doc.comment = comment.name
        doc.flags.ignore_mandatory = True
        doc.save()


def bg_message_contact_generation():
    message = frappe.db.get_list(
        "WhatsApp Message",
        or_filters=[
            {"link_to": ('is', 'not set')},
            {"link_name": ('is', 'not set')},
            {"contact": ('is', 'not set')}
        ],
        fields=["name", "to", "from"],
    )
    for msg in message:
        contact = msg.get("to") if msg.get("to") else msg.get("from")
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
                                AND cp.phone = '{contact}'
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
        if not contact_details:
            continue
        # print(contact_details)
        whatsapp_message = frappe.get_doc("WhatsApp Message", msg.get("name"))
        whatsapp_message.link_to = contact_details[0].get("link_doctype", "")
        whatsapp_message.link_name = contact_details[0].get("link_name", "")
        whatsapp_message.contact = contact_details[0].get("name", "")
        whatsapp_message.save()