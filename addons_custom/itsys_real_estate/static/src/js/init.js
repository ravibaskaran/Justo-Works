/** @odoo-module **/

/**
 * @Author: D.Jane
 * @Email: jane.odoo.sp@gmail.com
 *
 * Google Maps API Initialization for Odoo 18
 * Loads Google Maps JavaScript API with API key from configuration
 */

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";

/**
 * Initialize Google Maps API
 */
async function initGoogleMapsAPI(env) {
    const defaultKey = 'AIzaSyCLe7MRT7q5Rkd3kuyOoNSLb7wL-bk0Ip4';

    try {
        // Get API key from configuration
        const result = await env.services.rpc("/web/dataset/call_kw", {
            model: 'gmap.config',
            method: 'get_key_api',
            args: [],
            kwargs: {},
        });

        const apiKey = result || defaultKey;

        // Load Google Maps API
        const mapsUrl = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&sensor=true`;

        await loadJS(mapsUrl);

        console.log('Google Maps API loaded successfully');
    } catch (error) {
        console.error('Failed to load Google Maps API:', error);

        // Fallback: Try loading with default key
        const fallbackUrl = `https://maps.googleapis.com/maps/api/js?key=${defaultKey}&libraries=places&sensor=true`;

        try {
            await loadJS(fallbackUrl);
            console.log('Google Maps API loaded with default key');
        } catch (fallbackError) {
            console.error('Failed to load Google Maps API with default key:', fallbackError);
        }
    }
}

// Register as a service that runs on web client start
registry.category("services").add("google_maps_init", {
    start(env) {
        // Initialize Google Maps when the service starts
        initGoogleMapsAPI(env);
        return {};
    },
});