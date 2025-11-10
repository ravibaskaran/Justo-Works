/** @odoo-module **/

/**
 * MIGRATION NOTE: This file requires careful review for Odoo 18 compatibility
 *
 * This file overrides core Python evaluation utilities from Odoo.
 * In Odoo 18, the Python evaluation system has changed significantly.
 *
 * TODO:
 * 1. Check if this functionality is still needed in Odoo 18
 * 2. Review if domain field evaluation works differently in v18
 * 3. Test thoroughly if this custom evaluation is required
 * 4. Consider if this can be removed entirely if v18 handles it natively
 *
 * ORIGINAL PURPOSE:
 * - Overrides py_utils.eval to handle domain fields specially
 * - Allows using field values as domains in evaluation context
 * - Wraps JavaScript objects for Python evaluation
 *
 * STATUS: NEEDS REVIEW - May not be compatible or necessary in Odoo 18
 */

// ORIGINAL ODOO 15 CODE PRESERVED FOR REFERENCE
// This code is commented out and requires migration review

/*
odoo.define('web.domain_field', function (require) {
    "use strict";

    var py_utils = require('web.py_utils');
    var session = require('web.session');

    // ... (original code preserved but not migrated yet) ...
    // See git history for original implementation
});
*/

console.warn(
    'pyeval.js: This file contains custom Python evaluation overrides ' +
    'that need review for Odoo 18 compatibility. ' +
    'Please verify if this functionality is still required.'
);
