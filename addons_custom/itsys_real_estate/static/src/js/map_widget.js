/** @odoo-module **/

/**
 * @Author: D.Jane
 * @Email: jane.odoo.sp@gmail.com
 *
 * Google Maps Widget for Odoo 18
 * Provides interactive map with marker placement and dragging
 */

import { Component, onMounted, useRef, useState } from "@odoo/owl";

export class MapWidget extends Component {
    static template = "itsys_real_estate.google_map";

    setup() {
        this.state = useState({
            lat: this.props.lat || 0,
            lng: this.props.lng || 0,
        });

        this.mapRef = useRef("gmap-container");
        this.map = null;
        this.marker = null;

        onMounted(() => {
            this.onReady();
        });
    }

    /**
     * Initialize Google Maps after component is mounted
     */
    onReady() {
        const mapContainer = this.mapRef.el;

        if (!mapContainer) {
            return;
        }

        // Check if Google Maps API is loaded
        if (typeof google === 'undefined' || !google.maps) {
            console.error('Google Maps API is not loaded');
            return;
        }

        // Default latLng
        const latLng = new google.maps.LatLng(this.state.lat, this.state.lng);

        const mapOptions = {
            zoom: 12,
            center: latLng
        };

        this.map = new google.maps.Map(mapContainer, mapOptions);

        this.marker = new google.maps.Marker({
            position: latLng,
            map: this.map,
            draggable: true
        });

        // Map click event
        this.map.addListener('click', (event) => {
            const lat = event.latLng.lat();
            const lng = event.latLng.lng();

            // Update marker position
            const newLatLng = new google.maps.LatLng(lat, lng);
            this.marker.setPosition(newLatLng);
            google.maps.event.trigger(this.map, 'resize');

            // Update state and notify parent
            this.updatePlace(lat, lng);
        });

        // Right click event for debugging
        this.map.addListener('rightclick', (event) => {
            alert(`Lat: ${event.latLng.lat()}, Lng: ${event.latLng.lng()}`);
        });

        // Marker drag event
        this.marker.addListener('dragend', (event) => {
            const lat = event.latLng.lat();
            const lng = event.latLng.lng();
            this.updatePlace(lat, lng);
        });
    }

    /**
     * Toggle map visibility
     */
    onMapToggle() {
        const mapContainer = this.mapRef.el;
        if (mapContainer) {
            mapContainer.style.display =
                mapContainer.style.display === 'none' ? 'block' : 'none';

            // Update marker position when showing map
            if (mapContainer.style.display !== 'none') {
                this.updateMarker(this.state.lat, this.state.lng);
            }
        }
    }

    /**
     * Update marker position on the map
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     */
    updateMarker(lat, lng) {
        if (!this.map || !this.marker) {
            return;
        }

        this.state.lat = lat;
        this.state.lng = lng;

        const latLng = new google.maps.LatLng(lat, lng);
        this.map.setCenter(latLng);
        this.marker.setPosition(latLng);
        google.maps.event.trigger(this.map, 'resize');
    }

    /**
     * Update place coordinates and notify parent component
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     */
    updatePlace(lat, lng) {
        this.state.lat = lat;
        this.state.lng = lng;

        // Call parent's update method if provided
        if (this.props.onUpdatePlace) {
            this.props.onUpdatePlace(lat, lng);
        }
    }
}

MapWidget.props = {
    lat: { type: Number, optional: true },
    lng: { type: Number, optional: true },
    onUpdatePlace: { type: Function, optional: true },
};
