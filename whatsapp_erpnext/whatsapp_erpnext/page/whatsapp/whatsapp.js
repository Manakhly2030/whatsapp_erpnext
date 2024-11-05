frappe.pages["whatsapp"].on_page_show = function (wrapper) {
	load_whatsapp(wrapper);
  };
  
  const load_whatsapp = (wrapper) => {
	frappe.require(["whatsapp.bundle.js"], () => {
	  // Check if the module was loaded correctly
	  if (window.Whatsapp) {
		console.log("Whatsapp module loaded successfully!");
		new window.Whatsapp({ wrapper });
	  } else {
		console.error("Failed to load the Whatsapp class.");
	  }
	});
  };
  