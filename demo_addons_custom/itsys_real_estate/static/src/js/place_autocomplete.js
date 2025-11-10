/** @odoo-module **/

/**
 * @Author: D.Jane
 * @Email: jane.odoo.sp@gmail.com
 *
 * Google Places Autocomplete Field for Odoo 18
 * Provides address autocomplete with integrated map widget
 */

import { Component, onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { MapWidget } from "./map_widget";

export class PlaceAutocompleteField extends Component {
    static template = "itsys_real_estate.PlaceAutocompleteField";
    static components = { MapWidget };
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.inputRef = useRef("input");
        this.state = useState({
            lat: 50.862117,  // Default: Brussels
            lng: 4.416593,
            isMapVisible: false,
        });

        this.autocomplete = null;
        this.checkInterval = null;

        onMounted(() => {
            this.initAutocomplete();
        });

        onWillUnmount(() => {
            if (this.checkInterval) {
                clearInterval(this.checkInterval);
            }
        });
    }

    /**
     * Initialize Google Places Autocomplete
     * Waits for Google Maps API to be loaded
     */
    initAutocomplete() {
        // Check if Google Maps API is already loaded
        if (typeof google !== 'undefined' && google.maps && google.maps.places) {
            this.onReady();
        } else {
            // Wait for Google Maps API to load
            this.checkInterval = setInterval(() => {
                if (typeof google !== 'undefined' && google.maps && google.maps.places) {
                    this.onReady();
                }
            }, 1000);
        }
    }

    /**
     * Setup autocomplete and geocoder after Google API is loaded
     */
    onReady() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }

        const input = this.inputRef.el;
        if (!input) {
            return;
        }

        // Initialize geocoder to get lat/lng from current address
        const currentAddress = this.props.record.data[this.props.name] || '';
        if (currentAddress) {
            const geocoder = new google.maps.Geocoder();
            geocoder.geocode({ address: currentAddress }, (results, status) => {
                if (status === 'OK' && results[0]) {
                    this.state.lat = results[0].geometry.location.lat();
                    this.state.lng = results[0].geometry.location.lng();
                }
            });
        }

        // Initialize autocomplete
        this.autocomplete = new google.maps.places.Autocomplete(input, {
            types: ['geocode']
        });

        // Listen for place selection
        this.autocomplete.addListener('place_changed', () => {
            const place = this.autocomplete.getPlace();

            if (!place.geometry || !place.geometry.location) {
                return;
            }

            const location = place.geometry.location;
            this.state.lat = location.lat();
            this.state.lng = location.lng();

            // Update field value
            this.updateFieldValue(place.formatted_address || input.value);
        });
    }

    /**
     * Handle input change
     */
    onInputChange(ev) {
        const value = ev.target.value;
        this.updateFieldValue(value);
    }

    /**
     * Update field value in the record
     */
    updateFieldValue(value) {
        this.props.record.update({
            [this.props.name]: value,
        });
    }

    /**
     * Update place from map coordinates (reverse geocoding)
     */
    onUpdatePlace(lat, lng) {
        if (lat === this.state.lat && lng === this.state.lng) {
            return;
        }

        this.state.lat = lat;
        this.state.lng = lng;

        const geocoder = new google.maps.Geocoder();
        const latLng = new google.maps.LatLng(lat, lng);

        geocoder.geocode({ location: latLng }, (results, status) => {
            if (status === 'OK' && results[0]) {
                const address = results[0].formatted_address;
                this.updateFieldValue(address);

                // Update input element
                const input = this.inputRef.el;
                if (input) {
                    input.value = address;
                }
            }
        });
    }

    /**
     * Toggle map visibility
     */
    toggleMap() {
        this.state.isMapVisible = !this.state.isMapVisible;
    }

    get fieldValue() {
        return this.props.record.data[this.props.name] || '';
    }
}

PlaceAutocompleteField.displayName = "Place Autocomplete";

registry.category("fields").add("place_autocomplete", PlaceAutocompleteField);