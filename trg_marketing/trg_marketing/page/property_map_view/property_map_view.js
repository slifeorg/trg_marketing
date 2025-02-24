frappe.pages['property-map-view'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Property Map View',
        single_column: true
    });

    frappe.property_map_view = new PropertyMapView(page);
};

class PropertyMapView {
    constructor(page) {
        this.page = page;
        this.make();
    }

    make() {
        this.$container = $('<div>').appendTo(this.page.main);
        this.$map = $('<div>')
            .css({
                height: '500px',
                width: '100%',
                marginBottom: '20px'
            })
            .appendTo(this.$container);

        this.markers = [];
        this.initialize_map();
        this.load_properties();
    }

    initialize_map() {
        this.map = new google.maps.Map(this.$map[0], {
            center: { lat: 37.0902, lng: -95.7129 }, // US center
            zoom: 4
        });
    }

    load_properties() {
        const property_details = frappe.route_options.property_details || [];
        
        frappe.call({
            method: 'trg_marketing.trg_marketing.page.property_map_view.property_map_view.get_property_locations',
            args: {
                properties: property_details
            },
            callback: (r) => {
                if (r.message) {
                    this.plot_properties(r.message);
                }
            }
        });
    }

    plot_properties(properties) {
        const bounds = new google.maps.LatLngBounds();
        
        properties.forEach(prop => {
            if (prop.latitude && prop.longitude) {
                const marker = new google.maps.Marker({
                    position: { 
                        lat: parseFloat(prop.latitude), 
                        lng: parseFloat(prop.longitude) 
                    },
                    map: this.map,
                    title: `Built in ${prop.year_built}`
                });

                bounds.extend(marker.getPosition());
                this.markers.push(marker);

                // Add info window
                const infowindow = new google.maps.InfoWindow({
                    content: `
                        <div>
                            <h4>Property Details</h4>
                            <p>Year Built: ${prop.year_built}</p>
                            <p>Lead: <a href="/app/lead/${prop.lead}">${prop.lead}</a></p>
                        </div>
                    `
                });

                marker.addListener('click', () => {
                    infowindow.open(this.map, marker);
                });
            }
        });

        if (this.markers.length > 0) {
            this.map.fitBounds(bounds);
        }
    }
}