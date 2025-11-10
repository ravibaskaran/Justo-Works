/** @odoo-module **/

/**
 * Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
 * Odoo Proprietary License v1.0
 *
 * Migrated to Odoo 18 OWL Framework
 *
 * Image Swiper Backend for Odoo 18
 * Provides image carousel functionality for binary image fields using Brazzers Carousel
 */

import { ImageField } from "@web/views/fields/image/image_field";
import { patch } from "@web/core/utils/patch";
import { onPatched } from "@odoo/owl";

patch(ImageField.prototype, {
    setup() {
        super.setup(...arguments);

        onPatched(() => {
            if (this.props.readonly) {
                this.renderImageSwiper();
            }
        });
    },

    /**
     * Render image swiper carousel
     */
    renderImageSwiper() {
        const props = this.props;
        const record = props.record;

        if (!record) {
            return;
        }

        let relatedField = null;
        let relatedData = null;

        // Check if swipe_field option is set
        if (props.options?.swipe_field) {
            const swipeField = props.options.swipe_field;
            if (record.data[swipeField]) {
                relatedField = swipeField;
                relatedData = record.data[swipeField];
            }
        }
        // Default: check for property_template_image_ids
        else if (record.data.property_template_image_ids) {
            relatedField = 'property_template_image_ids';
            relatedData = record.data.property_template_image_ids;
        }

        if (!relatedData || !relatedData.records) {
            return;
        }

        const imageIds = relatedData.records;
        if (imageIds.length === 0) {
            return;
        }

        // Get image dimensions
        const width = props.options?.size?.[0] || props.width || 128;
        const height = props.options?.size?.[1] || props.height || 128;
        const timestamp = new Date().getTime().toString();

        // Get container
        const container = this.el?.querySelector('.o_field_image');
        if (!container) {
            return;
        }

        // Create images for carousel
        imageIds.forEach((imageRecord, index) => {
            const imageId = imageRecord.resId;
            const model = relatedData.resModel;

            const img = document.createElement('img');
            img.id = index.toString();
            img.dataset.id = imageId;
            img.src = `/web/image?model=${model}&field=image_${width}&id=${imageId}&unique=${timestamp}#`;
            img.style.maxWidth = `${width}px`;
            img.style.maxHeight = `${height}px`;
            img.style.margin = 'auto';

            container.appendChild(img);
        });

        // Initialize Brazzers Carousel if available
        if (typeof jQuery !== 'undefined' && jQuery.fn.brazzersCarousel) {
            const $container = jQuery(container);
            const swiper = $container.brazzersCarousel();

            // Add click handler for image viewer
            if (swiper) {
                swiper.parent().on('click', (e) => {
                    this.openImageViewer(e, relatedData, imageIds, width, timestamp);
                });
            }
        }
    },

    /**
     * Open image viewer for clicked image
     */
    openImageViewer(event, relatedData, imageIds, width, timestamp) {
        const $target = jQuery(event.currentTarget);
        const $currentDiv = $target.find("div.active");
        const $allImg = $target.closest(".brazzers-daddy").find("img");
        const $currentImg = $allImg.eq($currentDiv.index());

        const props = this.props;
        const record = props.record;

        // Build attachments array for viewer
        const attachments = [];

        // Add main image
        let mainImageId = `${record.resModel}/${record.resId}/${props.name}?unique=${Date.now()}#`;
        attachments.push({
            filename: record.data.display_name || '',
            id: mainImageId,
            is_main: true,
            mimetype: "image/jpeg",
            name: record.data.display_name || '',
            type: "image",
        });

        // Add related images
        imageIds.forEach((imageRecord, index) => {
            const imageId = imageRecord.resId;
            const model = relatedData.resModel;
            const imageUrl = `?model=${model}&field=image_1920&id=${imageId}&unique=${timestamp}#`;

            attachments.push({
                filename: index.toString(),
                id: imageUrl,
                is_main: true,
                mimetype: "image/jpeg",
                name: props.options?.swipe_field || 'property_template_image_ids',
                type: "image",
            });
        });

        // Determine which image was clicked
        const clickedImageId = $currentImg.data('id');
        if (clickedImageId >= 0) {
            const model = relatedData.resModel;
            mainImageId = `?model=${model}&field=image_1920&id=${clickedImageId}&unique=${timestamp}#`;
        }

        // Open document viewer (if available in Odoo 18)
        // Note: Document viewer implementation may vary in Odoo 18
        // This is a placeholder that may need adjustment based on actual Odoo 18 API
        if (window.DocumentViewer) {
            const viewer = new window.DocumentViewer(this, attachments, mainImageId);
            viewer.appendTo(document.body);
        }
    }
});
