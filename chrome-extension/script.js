const server_version = window?.odoo?.info?.server_version;

window.postMessage({ type: 'ODOO_VERSION', server_version }, '*');
