frappe.ui.form.on("Notification", {
    channel: function (frm) {
        if(frm.doc.channel == "WhatsApp"){
            frm.doc.message = null
        }
    }
})