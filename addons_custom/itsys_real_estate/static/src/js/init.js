/** @odoo-module **/

/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
* Migrated to Odoo 18 OWL - 2025-11-10
* SECURITY FIX: Changed HTTP → HTTPS for Google Maps API
*/

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";

// Google Maps API Loader Service
export const googleMapsService = {
    dependencies: ["orm"],

    start(env, { orm }) {
        // Default API key (should be moved to ir.config_parameter)
        const defaultKey = 'AIzaSyCLe7MRT7q5Rkd3kuyOoNSLb7wL-bk0Ip4';

        return orm.call('gmap.config', 'get_key_api', []).then((key) => {
            const apiKey = key || defaultKey;

            // SECURITY FIX: Changed HTTP → HTTPS
            const scriptUrl = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&sensor=true`;

            // Load Google Maps API script
            return loadJS(scriptUrl).catch((error) => {
                console.error('Failed to load Google Maps API:', error);
                throw error;
            });
        }).catch((error) => {
            console.warn('Failed to get Google Maps API key from config, using default:', error);

            // Fallback: load with default key
            const scriptUrl = `https://maps.googleapis.com/maps/api/js?key=${defaultKey}&libraries=places&sensor=true`;
            return loadJS(scriptUrl);
        });
    },
};

registry.category("services").add("googleMaps", googleMapsService);
