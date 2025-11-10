/** @odoo-module **/

/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
* Migrated to Odoo 18 OWL - 2025-11-10
*/

import { Component, useRef, onMounted, useState } from "@odoo/owl";

export class MapWidgetMulti extends Component {
    static template = "itsys_real_estate.google_map_multi";

    setup() {
        this.mapContainerRef = useRef("mapContainer");
        this.state = useState({
            mapVisible: false
        });

        // Get parent data
        this.latlngList = this.props.latlngList || [];
        this.lat = this.props.lat || 30.04300466950456;
        this.lng = this.props.lng || 31.235621482518354;

        // Store map and markers
        this.map = null;
        this.markers = [];

        onMounted(() => {
            this.onReady();
        });
    }

    toggleMap() {
        this.state.mapVisible = !this.state.mapVisible;
        const container = this.mapContainerRef.el;
        if (container) {
            container.style.display = this.state.mapVisible ? 'block' : 'none';
            if (this.state.mapVisible && this.map) {
                this.updateMarker(this.lat, this.lng);
            }
        }
    }

    onReady() {
        // Wait for Google Maps API to be available
        if (typeof google === 'undefined' || !google.maps) {
            console.warn('Google Maps API not loaded yet, retrying...');
            setTimeout(() => this.onReady(), 1000);
            return;
        }

        const container = this.mapContainerRef.el;
        if (!container) {
            console.error('Map container not found');
            return;
        }

        try {
            // Default latLng
            const latLng = new google.maps.LatLng(this.lat, this.lng);

            const mapOptions = {
                zoom: 16,
                center: latLng
            };

            // Create map
            this.map = new google.maps.Map(container, mapOptions);

            // Create multiple markers based on latlngList
            const latlngList = this.latlngList;
            for (let i = 0; i < latlngList.length; i++) {
                const item = latlngList[i];

                // Check if item has data and url
                if (item && item.data && item.data.url) {
                    // Determine marker icon based on state
                    let iconUrl = 'http://maps.google.com/mapfiles/ms/icons/';
                    const state = item.data.state;

                    if (state === 'free') {
                        iconUrl += 'green-dot.png';
                    } else if (state === 'reserved' || state === 'on_lease') {
                        iconUrl += 'blue-dot.png';
                    } else if (state === 'sold') {
                        iconUrl += 'red-dot.png';
                    } else {
                        iconUrl += 'red-dot.png'; // default
                    }

                    const url = item.data.url;
                    const markerLatLng = new google.maps.LatLng(item.data.lat, item.data.lng);

                    // Create marker
                    const marker = new google.maps.Marker({
                        url: url,
                        map: this.map,
                        position: markerLatLng,
                        draggable: false,
                        animation: google.maps.Animation.DROP,
                        icon: iconUrl
                    });

                    // Add click listener to navigate to URL
                    google.maps.event.addListener(marker, 'click', function () {
                        window.location.href = this.url;
                    });

                    this.markers.push(marker);
                }
            }

            // Map click event - show coordinates
            this.map.addListener('click', (event) => {
                alert('Lat: ' + event.latLng.lat() + ' , Lng: ' + event.latLng.lng());
            });

        } catch (error) {
            console.error('Error initializing Google Maps:', error);
        }
    }

    updateMarker(lat, lng) {
        if (!this.map) {
            console.warn('Map not initialized');
            return;
        }

        // For multi-marker map, just re-initialize
        this.onReady();
    }
}

MapWidgetMulti.props = {
    latlngList: { type: Array, optional: true },
    lat: { type: Number, optional: true },
    lng: { type: Number, optional: true },
};
