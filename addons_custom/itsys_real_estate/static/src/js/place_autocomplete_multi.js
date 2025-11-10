/** @odoo-module **/

/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
* Migrated to Odoo 18 OWL - 2025-11-10
*/

import { Component, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { MapWidgetMulti } from "./map_widget_multi";

export class PlaceAutocompleteMultiField extends Component {
    static template = "web.FieldText"; // Use standard text field template
    static components = { MapWidgetMulti };
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.inputRef = useRef("input");

        // Get latlng_ids data from parent record
        const latlngIds = this.props.record.data.latlng_ids;
        let defaultLat = 30.04300466950456;
        let defaultLng = 31.235621482518354;

        if (latlngIds && latlngIds.records && latlngIds.records.length > 0) {
            const firstRecord = latlngIds.records[0];
            if (firstRecord.data) {
                defaultLat = firstRecord.data.lat || defaultLat;
                defaultLng = firstRecord.data.lng || defaultLng;
            }
        }

        this.lat = defaultLat;
        this.lng = defaultLng;
        this.latlngList = this.prepareLatlngList(latlngIds);

        // Store references
        this.autocomplete = null;
        this.geocoder = null;
        this.mapWidgetComponent = null;

        onMounted(() => {
            this.initAutocomplete();
        });
    }

    prepareLatlngList(latlngIds) {
        if (!latlngIds || !latlngIds.records) {
            return [];
        }

        // Convert records to the format expected by MapWidgetMulti
        return latlngIds.records.map(record => ({
            data: record.data
        }));
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

    // Render MapWidgetMulti as a child component
    get mapWidgetProps() {
        return {
            latlngList: this.latlngList,
            lat: this.lat,
            lng: this.lng
        };
    }
}

registry.category("fields").add("place_autocomplete_multi", PlaceAutocompleteMultiField);
