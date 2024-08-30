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