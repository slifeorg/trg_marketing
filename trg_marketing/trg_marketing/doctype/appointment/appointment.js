frappe.ui.form.on('Appointment', {
	refresh(frm) {
		console.log("test")
		$(".control-input:has(select) use[href='#icon-select']")
			.attr("href", "#icon-arrow-down-trg")

		initGeocoder().then(() => {
			if (frm.fields_dict['custom_street']) {
				const input = frm.fields_dict['custom_street'].input;
				const inputWrapper = $(input).closest('.control-input');
				
				inputWrapper.css('position', 'relative');
				
				const suggestionsContainer = $('<div>')
					.addClass('suggestions')
					.css({
						'display': 'none',
						'position': 'absolute',
						'z-index': '1000',
						'background-color': 'white',
						'box-shadow': '0 2px 5px rgba(0,0,0,0.2)',
						'width': '100%',
						'max-height': '200px',
						'overflow-y': 'auto',
						'border': '1px solid #ccc',
						'border-radius': '4px',
						'bottom': '0',
						'left': '0',
						'transform': 'translateY(100%)'
					})
					.appendTo(inputWrapper);
				
				const geocoder = L.Control.Geocoder.nominatim();
				
				$(input).data('geocoder', geocoder);
				$(input).data('suggestions', suggestionsContainer);
			}
			console.log("Geocoder inzialized");
		}).catch(() => {
			console.error("Error initializing geocoder");
		});
	},
	custom_street(frm) {
		const input = frm.fields_dict['custom_street'].input;
		const geocoder = $(input).data('geocoder');
		const suggestionsContainer = $(input).data('suggestions');
		
		if (!geocoder || !suggestionsContainer) return;
		
		const query = $(input).val().trim();
		
		if (!query) {
			suggestionsContainer.html('').hide();
			return;
		}
		
		geocoder.geocode(query).then(results => {
			suggestionsContainer.html('');
			
			if (!results || results.length === 0) {
				suggestionsContainer.hide();
				return;
			}
			
			suggestionsContainer.show();
			
			results.forEach(function(result) {
				console.log(result)
				$('<div>')
					.addClass('suggestion-item')
					.text(result.name)
					.css({
						'padding': '8px 12px',
						'cursor': 'pointer'
					})
					.hover(
						function() { $(this).css('background-color', '#f0f0f0'); },
						function() { $(this).css('background-color', 'transparent'); }
					)
					.on('click', function() {
						$(input).val(result.name);
						
						suggestionsContainer.hide();
						
						const lat = result.center.lat;
						const lng = result.center.lng;
						
						const address = result.properties.address || {};

						if (frm.fields_dict['latitude']) 
							frm.set_value('latitude', lat);
						if (frm.fields_dict['longitude']) 
							frm.set_value('longitude', lng);
						if (frm.fields_dict['custom_city'] && address.city) 
							frm.set_value('custom_city', address.city);
						if (frm.fields_dict['custom_state'] && address.state) 
							frm.set_value('custom_state', address.state);
						if (frm.fields_dict['custom_zipcode'] && address.postcode) 
							frm.set_value('custom_zipcode', address.postcode);
					})
					.appendTo(suggestionsContainer);
			});
		});
	}
})

async function initGeocoder() {
	return new Promise((resolve, reject) => {
		try {
			if (typeof L !== 'undefined' && typeof L.Control.Geocoder === 'undefined') {
				$.getScript('https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js')
					.done(function() {
						console.log('Control.Geocoder loaded');
						resolve();
					})
					.fail(function(err) {
						console.error('Error loading Geocoder JS:', err);
						reject();
					});
			}
		} catch (e) {
			console.error('Error initializing libraries:', e);
			reject();
		}
	});
}