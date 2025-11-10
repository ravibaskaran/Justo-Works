/** @odoo-module **/

/**
 * @Author: D.Jane
 * @Email: jane.odoo.sp@gmail.com
 *
 * Google Places Autocomplete with Multi-Marker Map for Odoo 18
 * Displays autocomplete with map showing multiple location markers
 */

import { Component, onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { MapWidgetMulti } from "./map_widget_multi";

export class PlaceAutocompleteMultiField extends Component {
    static template = "itsys_real_estate.PlaceAutocompleteMultiField";
    static components = { MapWidgetMulti };
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.inputRef = useRef("input");

        // Get initial coordinates from latlng_ids if available
        const latlngData = this.props.record.data.latlng_ids?.records || [];
        const defaultLat = latlngData.length > 0 ? latlngData[0].data.lat : 30.04300466950456;
        const defaultLng = latlngData.length > 0 ? latlngData[0].data.lng : 31.235621482518354;

        this.state = useState({
            lat: defaultLat,
            lng: defaultLng,
            latlngList: latlngData,
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
     */
    initAutocomplete() {
        if (typeof google !== 'undefined' && google.maps && google.maps.places) {
            this.onReady();
        } else {
            this.checkInterval = setInterval(() => {
                if (typeof google !== 'undefined' && google.maps && google.maps.places) {
                    this.onReady();
                }
            }, 1000);
        }
    }

    /**
     * Setup autocomplete after Google API is loaded
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

        // Initialize geocoder for current address
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

PlaceAutocompleteMultiField.displayName = "Place Autocomplete Multi";

registry.category("fields").add("place_autocomplete_multi", PlaceAutocompleteMultiField);