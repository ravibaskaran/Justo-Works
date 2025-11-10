/** @odoo-module **/

/**
 * @Author: D.Jane
 * @Email: jane.odoo.sp@gmail.com
 *
 * Multi-Marker Google Maps Widget for Odoo 18
 * Displays multiple location markers with different states
 */

import { Component, onMounted, useRef, useState } from "@odoo/owl";

export class MapWidgetMulti extends Component {
    static template = "itsys_real_estate.google_map_multi";

    setup() {
        this.state = useState({
            lat: this.props.lat || 0,
            lng: this.props.lng || 0,
        });

        this.mapRef = useRef("gmap-container-multi");
        this.map = null;
        this.markers = [];
        this.latlngList = this.props.latlngList || [];

        onMounted(() => {
            this.onReady();
        });
    }

    /**
     * Get marker icon URL based on property state
     * @param {string} state - Property state (free, reserved, on_lease, sold)
     * @returns {string} Icon URL
     */
    getMarkerIcon(state) {
        const baseUrl = 'http://maps.google.com/mapfiles/ms/icons/';
        const iconMap = {
            'free': 'green-dot.png',
            'reserved': 'blue-dot.png',
            'on_lease': 'blue-dot.png',
            'sold': 'red-dot.png'
        };
        return baseUrl + (iconMap[state] || 'red-dot.png');
    }

    /**
     * Initialize Google Maps with multiple markers
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

        // Clear existing markers
        this.clearMarkers();

        // Default center latLng
        const centerLatLng = new google.maps.LatLng(this.state.lat, this.state.lng);

        const mapOptions = {
            zoom: 16,
            center: centerLatLng
        };

        this.map = new google.maps.Map(mapContainer, mapOptions);

        // Add markers for each location
        this.latlngList.forEach((item) => {
            const data = item.data || item;

            if (data.url) {
                const icon = this.getMarkerIcon(data.state);
                const position = new google.maps.LatLng(data.lat, data.lng);

                const marker = new google.maps.Marker({
                    map: this.map,
                    position: position,
                    draggable: false,
                    animation: google.maps.Animation.DROP,
                    icon: icon
                });

                // Add click listener to navigate to property URL
                marker.addListener('click', () => {
                    if (data.url) {
                        window.location.href = data.url;
                    }
                });

                this.markers.push(marker);
            }
        });

        // Map click event for debugging
        this.map.addListener('click', (event) => {
            alert(`Lat: ${event.latLng.lat()}, Lng: ${event.latLng.lng()}`);
        });
    }

    /**
     * Clear all markers from the map
     */
    clearMarkers() {
        this.markers.forEach(marker => {
            marker.setMap(null);
        });
        this.markers = [];
    }

    /**
     * Toggle map visibility
     */
    onMapToggle() {
        const mapContainer = this.mapRef.el;
        if (mapContainer) {
            mapContainer.style.display =
                mapContainer.style.display === 'none' ? 'block' : 'none';

            // Refresh markers when showing map
            if (mapContainer.style.display !== 'none') {
                this.updateMarkers();
            }
        }
    }

    /**
     * Update/refresh all markers on the map
     */
    updateMarkers() {
        this.onReady();
    }
}

MapWidgetMulti.props = {
    lat: { type: Number, optional: true },
    lng: { type: Number, optional: true },
    latlngList: { type: Array, optional: true },
};
