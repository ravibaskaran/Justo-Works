/** @odoo-module **/

/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
* Migrated to Odoo 18 OWL - 2025-11-10
*/

import { Component, useRef, onMounted, useState } from "@odoo/owl";

export class MapWidget extends Component {
    static template = "itsys_real_estate.google_map";

    setup() {
        this.mapContainerRef = useRef("mapContainer");
        this.state = useState({
            mapVisible: false
        });

        // Get parent data
        this.lat = this.props.lat || 50.862117;
        this.lng = this.props.lng || 4.416593;

        // Store map and marker references
        this.map = null;
        this.marker = null;

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
                zoom: 12,
                center: latLng
            };

            // Create map
            this.map = new google.maps.Map(container, mapOptions);

            // Create marker
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

                // Notify parent to update place
                if (this.props.onUpdatePlace) {
                    this.props.onUpdatePlace(lat, lng);
                }
            });

            // Map right-click event
            this.map.addListener('rightclick', (event) => {
                alert('Lat: ' + event.latLng.lat() + ' , Lng: ' + event.latLng.lng());
            });

            // Marker drag event
            this.marker.addListener('dragend', (event) => {
                const lat = event.latLng.lat();
                const lng = event.latLng.lng();

                // Notify parent to update place
                if (this.props.onUpdatePlace) {
                    this.props.onUpdatePlace(lat, lng);
                }
            });

        } catch (error) {
            console.error('Error initializing Google Maps:', error);
        }
    }

    updateMarker(lat, lng) {
        if (!this.map || !this.marker) {
            console.warn('Map or marker not initialized');
            return;
        }

        this.lat = lat;
        this.lng = lng;

        const latLng = new google.maps.LatLng(lat, lng);
        this.map.setCenter(latLng);
        this.marker.setPosition(latLng);
        google.maps.event.trigger(this.map, 'resize');
    }
}

MapWidget.props = {
    lat: { type: Number, optional: true },
    lng: { type: Number, optional: true },
    onUpdatePlace: { type: Function, optional: true },
};
