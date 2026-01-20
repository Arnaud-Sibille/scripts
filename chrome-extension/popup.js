chrome.storage.local.get('server_version').then(result => {
    document.getElementById("server-version").textContent = result.server_version ?? '';
});
