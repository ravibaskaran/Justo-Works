/** @odoo-module **/

/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
* Migrated to Odoo 18 OWL - 2025-11-10
*/

import { Component, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { MapWidget } from "./map_widget";

export class PlaceAutocompleteField extends Component {
    static template = "web.FieldText"; // Use standard text field template
    static components = { MapWidget };
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.inputRef = useRef("input");

        // Default coordinates (Brussels, Belgium)
        this.lat = 50.862117;
        this.lng = 4.416593;

        // Store references
        this.autocomplete = null;
        this.geocoder = null;
        this.mapWidgetComponent = null;

        onMounted(() => {
            this.initAutocomplete();
        });
    }

    initAutocomplete() {
        // Wait for Google Maps API to be available
        if (typeof google === 'undefined' || !google.maps) {
            console.warn('Google Maps API not loaded yet, retrying...');
            setTimeout(() => this.initAutocomplete(), 1000);
            return;
        }

        try {
            const inputEl = this.inputRef.el;
            if (!inputEl) {
                console.error('Input element not found');
                return;
            }

            // Initialize geocoder
            this.geocoder = new google.maps.Geocoder();

            // Get current address value and geocode it
            const currentAddress = this.props.record.data[this.props.name] || '';
            if (currentAddress) {
                this.geocoder.geocode({ 'address': currentAddress }, (results, status) => {
                    if (status === 'OK' && results[0]) {
                        this.lat = results[0].geometry.location.lat();
                        this.lng = results[0].geometry.location.lng();
                    }
                });
            }

            // Initialize autocomplete
            this.autocomplete = new google.maps.places.Autocomplete(inputEl, {
                types: ['geocode']
            });

            // Listen for place selection
            this.autocomplete.addListener('place_changed', () => {
                const place = this.autocomplete.getPlace();

                if (!place.geometry || !place.geometry.location) {
                    console.warn('No geometry found for selected place');
                    return;
                }

                const location = place.geometry.location;
                this.lat = location.lat();
                this.lng = location.lng();

                // Update the map widget if it exists
                if (this.mapWidgetComponent) {
                    this.mapWidgetComponent.updateMarker(this.lat, this.lng);
                }

                // Update the field value
                this.updateFieldValue(place.formatted_address);
            });

        } catch (error) {
            console.error('Error initializing Google Places Autocomplete:', error);
        }
    }

    onUpdatePlace(lat, lng) {
        if (lat === this.lat && lng === this.lng) {
            return;
        }

        this.lat = lat;
        this.lng = lng;

        if (!this.geocoder) {
            console.warn('Geocoder not initialized');
            return;
        }

        // Reverse geocode to get address
        const latLng = new google.maps.LatLng(lat, lng);
        this.geocoder.geocode({ 'location': latLng }, (results, status) => {
            if (status === 'OK' && results[0]) {
                const formattedAddress = results[0].formatted_address;
                this.updateFieldValue(formattedAddress);
            }
        });
    }

    updateFieldValue(value) {
        // Update the field value in Odoo
        if (this.props.record.update) {
            this.props.record.update({
                [this.props.name]: value
            });
        }
    }

    // Render MapWidget as a child component
    get mapWidgetProps() {
        return {
            lat: this.lat,
            lng: this.lng,
            onUpdatePlace: this.onUpdatePlace.bind(this)
        };
    }
}

registry.category("fields").add("place_autocomplete", PlaceAutocompleteField);
