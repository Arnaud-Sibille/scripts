const script = document.createElement('script');
script.src = chrome.runtime.getURL('script.js');
(document.documentElement).appendChild(script);
script.onload = script.remove();

window.addEventListener('message', (event) => {
    if (event.data?.type === 'ODOO_VERSION') {
        if (event.data.server_version) {
            chrome.storage.local.set({ server_version: event.data.server_version });
        } else {
            chrome.storage.local.remove('server_version')
        }
    }
})
